import hashlib
import os
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_io_models.input_models import LoginInput, SignupInput
from api_io_models.output_models import MessageOut
from auth.auth_handler import (
    clear_auth_cookies,
    create_access_token,
    create_refresh_token,
    hash_password,
    set_auth_cookies,
    verify_password,
)
from common_messages.error_messages import ErrorMessages
from common_messages.success_messages import SuccessMessages
from database.database_handler import get_db
from database.database_models import RefreshToken, UserMaster, UserProfile

router = APIRouter(prefix="/auth", tags=["Auth"])

_REFRESH_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


@router.post(
    "/signup",
    response_model=MessageOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
    description=(
        "Creates a new user in user_master and an empty user_profile row. "
        "Sets HttpOnly access_token and refresh_token cookies on success."
    ),
    responses={
        409: {"description": "Email already registered"},
        422: {"description": "Validation error (e.g. password too short)"},
    },
)
async def signup(
    body: SignupInput, response: Response, db: AsyncSession = Depends(get_db)
):
    existing = await db.execute(select(UserMaster).where(UserMaster.email == body.email))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ErrorMessages.EMAIL_ALREADY_EXISTS.value,
        )

    user = UserMaster(email=body.email, password_hash=hash_password(body.password))
    db.add(user)
    await db.flush()

    db.add(UserProfile(user_id=user.id))
    await db.flush()

    raw_refresh, hashed_refresh = create_refresh_token()
    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=hashed_refresh,
            expires_at=datetime.now(timezone.utc) + timedelta(days=_REFRESH_EXPIRE_DAYS),
        )
    )

    access_token = create_access_token(user.id, user.email)
    set_auth_cookies(response, access_token, raw_refresh)
    return MessageOut(message=SuccessMessages.ACCOUNT_CREATED.value)


@router.post(
    "/login",
    response_model=MessageOut,
    summary="Login with email and password",
    description=(
        "Validates credentials and checks if account is disabled. "
        "Sets HttpOnly access_token and refresh_token cookies on success."
    ),
    responses={
        401: {"description": "Invalid credentials"},
        403: {"description": "Account disabled"},
    },
)
async def login(
    body: LoginInput, response: Response, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(UserMaster).where(UserMaster.email == body.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.INVALID_CREDENTIALS.value,
        )

    if user.is_account_disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorMessages.ACCOUNT_DISABLED.value,
        )

    raw_refresh, hashed_refresh = create_refresh_token()
    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=hashed_refresh,
            expires_at=datetime.now(timezone.utc) + timedelta(days=_REFRESH_EXPIRE_DAYS),
        )
    )

    access_token = create_access_token(user.id, user.email)
    set_auth_cookies(response, access_token, raw_refresh)
    return MessageOut(message=SuccessMessages.LOGIN_SUCCESS.value)


@router.post(
    "/refresh",
    response_model=MessageOut,
    summary="Refresh access token",
    description=(
        "Reads the refresh_token HttpOnly cookie, validates it against the database "
        "(not revoked, not expired), and issues a new access_token cookie."
    ),
    responses={
        401: {"description": "Refresh token missing, revoked, or expired"},
        403: {"description": "Account disabled"},
    },
)
async def refresh(
    response: Response,
    refresh_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.REFRESH_TOKEN_INVALID.value,
        )

    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.is_revoked.is_(False),
            RefreshToken.expires_at > datetime.now(timezone.utc),
        )
    )
    token_record = result.scalar_one_or_none()
    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.REFRESH_TOKEN_INVALID.value,
        )

    user_result = await db.execute(
        select(UserMaster).where(UserMaster.id == token_record.user_id)
    )
    user = user_result.scalar_one_or_none()
    if not user or user.is_account_disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorMessages.ACCOUNT_DISABLED.value,
        )

    new_access_token = create_access_token(user.id, user.email)
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")) * 60,
    )
    return MessageOut(message=SuccessMessages.TOKEN_REFRESHED.value)


@router.post(
    "/logout",
    response_model=MessageOut,
    summary="Logout and revoke refresh token",
    description=(
        "Marks the refresh token as revoked in the database so it cannot be used again, "
        "then clears both access_token and refresh_token cookies from the browser."
    ),
)
async def logout(
    response: Response,
    refresh_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
):
    if refresh_token:
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        result = await db.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        token_record = result.scalar_one_or_none()
        if token_record:
            token_record.is_revoked = True

    clear_auth_cookies(response)
    return MessageOut(message=SuccessMessages.LOGOUT_SUCCESS.value)
