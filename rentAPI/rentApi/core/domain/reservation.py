"""Modul containing car-related domain models."""


from enum import Enum
from pydantic import BaseModel, ConfigDict, UUID4
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

class ReservationBroker(ReservationIn):
    """A broker class including user in the model."""
    user_id: UUID4


class Reservation(ReservationBroker):
    """Model representing reservation's attributes."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
