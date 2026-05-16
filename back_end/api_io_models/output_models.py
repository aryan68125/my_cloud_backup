from typing import Optional

from pydantic import BaseModel


class MessageOut(BaseModel):
    message: str


class UserProfileOut(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

    model_config = {"from_attributes": True}


class UserMeOut(BaseModel):
    id: int
    email: str
    is_admin_user: bool
    profile: Optional[UserProfileOut]

    model_config = {"from_attributes": True}


class HelloOut(BaseModel):
    message: str
