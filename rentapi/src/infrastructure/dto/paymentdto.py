"""Module containing payment DTO."""

from typing import Any
from datetime import datetime
from src.core.domain.payment import PaymentStatus
from pydantic import BaseModel, ConfigDict


class PaymentDTO(BaseModel):
    """DTO for Payment model."""
    id: int
    reservation_id: int
    status: PaymentStatus
    amount: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_record(cls, record: Any) -> "PaymentDTO":
        """A method converting record to DTO.

        Args:
            record (Any): The record from the DB.

        Returns:
            PaymentDTO: The DTO object.
        """

        return cls(
            id=record["id"],
            reservation_id=record["reservation_id"],
            status=record["status"] or PaymentStatus.PENDING,
            amount=record["amount"],
            created_at=record["created_at"],
            updated_at=record["updated_at"],
        )
