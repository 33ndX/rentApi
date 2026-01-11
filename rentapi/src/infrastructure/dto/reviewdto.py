"""A module containing DTO models for output reviews."""

from datetime import datetime
from typing import Optional
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, UUID4


class ReviewDTO(BaseModel):
    """A model representing DTO for review data."""
    id: int
    user_id: UUID4
    car_id: int
    body: str
    rating: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True
    )

    @classmethod
    def from_record(cls, record: Record) -> "ReviewDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            ReviewDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),  # type: ignore
            user_id=record_dict.get("user_id"),  # type: ignore
            car_id=record_dict.get("car_id"),  # type: ignore
            body=record_dict.get("body"),  # type: ignore
            rating=record_dict.get("rating"),  # type: ignore
            created_at=record_dict.get("created_at"),
        )
