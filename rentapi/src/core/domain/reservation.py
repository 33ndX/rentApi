"""Modul containing reservation-related domain models."""

from enum import Enum
from pydantic import BaseModel, ConfigDict, field_validator, model_validator, UUID4, Field
from typing import Optional
from datetime import datetime, timezone


class ReservationStatus(str, Enum):
    """Status of the reservation."""
    PENDING = "PENDING_PAYMENT"
    CONFIRMED = "CONFIRMED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ReservationIn(BaseModel):
    """Model representing reservation's attributes."""
    car_id: int
    reservation_start: datetime = Field(
        ...,
        examples=["2026-01-01 12:00:00"]
    )
    reservation_end: datetime = Field(
        ...,
        examples=["2026-01-02 12:00:00"]
    )

    @field_validator("reservation_start", "reservation_end")
    def validate_reservation_date(cls, date: datetime) -> datetime:
        now = datetime.now(timezone.utc) if date.tzinfo else datetime.now()
        if date < now:
            raise ValueError("reservation date cannot be in the past")
        return date

    @model_validator(mode="after")
    def validate_reservation_period(self):
        if self.reservation_end <= self.reservation_start:
            raise ValueError('reservation_end must be after reservation_start')
        return self


class ReservationBroker(ReservationIn):
    """Broker class including user in the model."""
    user_id: UUID4


class Reservation(ReservationBroker):
    """Model representing reservation's attributes in the database."""
    id: int
    status: ReservationStatus = ReservationStatus.PENDING
    total_price: float
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True, extra="ignore")
