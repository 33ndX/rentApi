"""Modul containing review-related domain models."""

from pydantic import BaseModel, ConfigDict


class ReviewIn(BaseModel):
    """Model representing review's attributes."""
    car_id: int
    body: str


class Review(ReviewIn):
    """Model representing review's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
