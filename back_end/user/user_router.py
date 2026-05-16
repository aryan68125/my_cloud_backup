from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_io_models.input_models import UpdateProfileInput
from api_io_models.output_models import MessageOut, UserMeOut, UserProfileOut
from common_messages.success_messages import SuccessMessages
from database.database_handler import get_db
from database.database_models import UserMaster, UserProfile
from user.user_handler import get_current_user

router = APIRouter(prefix="/user", tags=["User"])


@router.get(
    "/me",
    response_model=UserMeOut,
    summary="Get current user info",
    description=(
        "Returns the authenticated user's id, email, admin status, and profile "
        "(first name, last name, phone). Requires a valid access_token cookie."
    ),
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Account disabled"},
    },
)
async def get_me(current_user: UserMaster = Depends(get_current_user)):
    profile_out = None
    if current_user.profile:
        profile_out = UserProfileOut(
            first_name=current_user.profile.first_name,
            last_name=current_user.profile.last_name,
            phone_number=current_user.profile.phone_number,
        )
    return UserMeOut(
        id=current_user.id,
        email=current_user.email,
        is_admin_user=current_user.is_admin_user,
        profile=profile_out,
    )


@router.put(
    "/me",
    response_model=MessageOut,
    summary="Update user profile",
    description="Updates first name, last name, and/or phone number. Only provided fields are updated.",
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Account disabled"},
    },
)
async def update_me(
    body: UpdateProfileInput,
    current_user: UserMaster = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not current_user.profile:
        db.add(UserProfile(user_id=current_user.id))
        await db.flush()

    if body.first_name is not None:
        current_user.profile.first_name = body.first_name
    if body.last_name is not None:
        current_user.profile.last_name = body.last_name
    if body.phone_number is not None:
        current_user.profile.phone_number = body.phone_number

    return MessageOut(message=SuccessMessages.PROFILE_UPDATED.value)


@router.delete(
    "/me",
    response_model=MessageOut,
    summary="Delete user account",
    description=(
        "Permanently deletes the authenticated user's account. "
        "Cascades to user_profile and all refresh_tokens rows."
    ),
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Account disabled"},
    },
)
async def delete_me(
    current_user: UserMaster = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await db.delete(current_user)
    return MessageOut(message=SuccessMessages.ACCOUNT_DELETED.value)
