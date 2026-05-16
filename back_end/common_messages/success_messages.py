from enum import Enum


class SuccessMessages(Enum):
    ACCOUNT_CREATED = "Account created successfully."
    LOGIN_SUCCESS = "Logged in successfully."
    LOGOUT_SUCCESS = "Logged out successfully."
    PROFILE_UPDATED = "Profile updated successfully."
    ACCOUNT_DELETED = "Account deleted successfully."
    TOKEN_REFRESHED = "Token refreshed successfully."
