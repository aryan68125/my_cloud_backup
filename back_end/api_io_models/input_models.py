from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


class SignupInput(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        return v


class LoginInput(BaseModel):
    email: EmailStr
    password: str


class UpdateProfileInput(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
