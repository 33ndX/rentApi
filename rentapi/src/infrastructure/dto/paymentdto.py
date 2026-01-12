"""Module containing payment DTO."""

from datetime import datetime
from asyncpg import Record  # type: ignore
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
    def from_record(cls, record: Record) -> "PaymentDTO":
        """A method converting record to DTO.

        Args:
            record (Any): The record from the DB.

        Returns:
            PaymentDTO: The DTO object.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),  # type: ignore
            reservation_id=record_dict.get("reservation_id"),  # type: ignore
            status=record_dict.get("status") or PaymentStatus.PENDING,  # type: ignore
            amount=record_dict.get("amount"),  # type: ignore
            created_at=record_dict.get("created_at"),
            updated_at=record_dict.get("updated_at"),
        )
