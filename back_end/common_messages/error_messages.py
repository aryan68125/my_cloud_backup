from enum import Enum


class ErrorMessages(Enum):
    INVALID_CREDENTIALS = "Invalid email or password."
    ACCOUNT_DISABLED = "Your account has been disabled. Please contact support."
    EMAIL_ALREADY_EXISTS = "An account with this email already exists."
    USER_NOT_FOUND = "User not found."
    INVALID_TOKEN = "Invalid or expired token."
    REFRESH_TOKEN_INVALID = "Refresh token is invalid or has been revoked."
    UNAUTHORIZED = "Authentication required."
