"""Modul containing reservation-related domain models."""


from enum import Enum
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ReservationStatus(str, Enum):
    """Status of the reservation."""
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class ReservationIn(BaseModel):
    """Model representing reservation's attributes."""
    car_id: int
    reservation_start: datetime
    reservation_end: datetime
    payment: float
    status: ReservationStatus


class Reservation(ReservationIn):
    """Model representing reservation's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
