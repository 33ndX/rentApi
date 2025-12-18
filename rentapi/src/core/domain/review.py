"""Modul containing review-related domain models."""

from pydantic import BaseModel, ConfigDict, field_validator, UUID4
from typing import Optional
from datetime import datetime



class ReviewIn(BaseModel):
    """Model representing review's attributes."""
    car_id: int
    reservation_id: int
    body: str
    rating: int

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, rating: int) -> int:
        """Validate rating between 1 and 5"""
        if rating not in range(1, 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating


class ReviewBroker(ReviewIn):
    """Broker class including user in the model."""
    user_id: UUID4


class Review(ReviewBroker):
    """Model representing review's attributes in the database."""
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True, extra="ignore")
