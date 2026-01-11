"""Module containing payment-related domain models."""

from enum import Enum
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PaymentStatus(str, Enum):
    """Status of the payment."""
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"


class PaymentIn(BaseModel):
    """Model representing payment's attributes for creation."""
    reservation_id: int
    amount: float


class Payment(PaymentIn):
    """Model representing payment's attributes in the database."""
    id: int
    status: PaymentStatus = PaymentStatus.PENDING
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")
