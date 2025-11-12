"""Modul containing review-related domain models."""

from pydantic import BaseModel, ConfigDict
from uuid import UUID


class ReviewIn(BaseModel):
    """Model representing review's attributes."""
    car_id: UUID
    body: str


class Review(ReviewIn):
    """Model representing review's attributes."""
    id: int
    user_id: UUID
    car_id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
