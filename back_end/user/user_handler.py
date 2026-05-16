from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from auth.auth_handler import verify_access_token
from common_messages.error_messages import ErrorMessages
from database.database_handler import get_db
from database.database_models import UserMaster


async def get_current_user(
    access_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
) -> UserMaster:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.UNAUTHORIZED.value,
        )

    payload = verify_access_token(access_token)
    user_id = int(payload["sub"])

    result = await db.execute(
        select(UserMaster)
        .options(selectinload(UserMaster.profile))
        .where(UserMaster.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.USER_NOT_FOUND.value,
        )

    if user.is_account_disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorMessages.ACCOUNT_DISABLED.value,
        )

    return user
