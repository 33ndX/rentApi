"""Modul containing payment-related domain models."""

from enum import Enum
from pydantic import BaseModel, ConfigDict, UUID1


class PaymentStatus(str, Enum):
    """Status of the payment."""
    PENDING = "Pending"
    COMPLETED = "Completed"


class PaymentIn(BaseModel):
    """Model representing payment's attributes."""
    price: float
    status: PaymentStatus
    reservation_id: int
    user_id: UUID1


class Payment(PaymentIn):
    """Model representing payment's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
