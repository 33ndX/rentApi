"""Model containing user-related models"""

from enum import Enum
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class UserRole(str, Enum):
    """Enum representing user roles"""
    ADMIN = "ADMIN"
    USER = "USER"


class UserIn(BaseModel):
    """An input user model."""
    email: str
    user_password: str
    role: UserRole = UserRole.USER


class User(UserIn):
    """The user model class"""
    id: UUID

    model_config = ConfigDict(from_attributes=True, extra="ignore")
