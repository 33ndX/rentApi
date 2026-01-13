"""A module containing DTO models for output reservations."""

from datetime import datetime
from typing import Optional
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, UUID4, field_serializer
from src.infrastructure.utils.serializers import serialize_datetime


from src.core.domain.reservation import ReservationStatus


class ReservationDTO(BaseModel):
    """A model representing DTO for reservation data."""
    id: int
    user_id: UUID4
    car_id: int
    reservation_start: datetime
    reservation_end: datetime
    status: ReservationStatus
    total_price: float
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True
    )

    @field_serializer("reservation_start", "reservation_end", "created_at")
    def serialize_dates(self, dt: datetime, _info):
        return serialize_datetime(dt)

    @classmethod
    def from_record(cls, record: Record) -> "ReservationDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            ReservationDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),  # type: ignore
            user_id=record_dict.get("user_id"),  # type: ignore
            car_id=record_dict.get("car_id"),  # type: ignore
            reservation_start=record_dict.get("reservation_start"),  # type: ignore
            reservation_end=record_dict.get("reservation_end"),  # type: ignore
            status=record_dict.get("reservation_status") or ReservationStatus.PENDING,  # type: ignore
            total_price=record_dict.get("total_price"),  # type: ignore
            created_at=record_dict.get("created_at"),
        )
