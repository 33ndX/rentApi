"""A module containing DTO models for payment"""
from pydantic import BaseModel, ConfigDict, UUID4  # type: ignore

from rentapi.src.core.domain.payment import PaymentStatus


class PaymentDTO(BaseModel):
    """A model representing a DTO for payment data"""
    id: int
    price: float
    status: PaymentStatus
    reservation_id: int
    user_id: UUID4

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )
