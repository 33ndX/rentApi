"""A module containing DTO models for output cars."""

from typing import Optional
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict


class CarDTO(BaseModel):
    """A model representing DTO for car data."""
    id: int
    brand: str
    model: str
    year: int
    price_per_day: float
    registration_number: str
    mileage: Optional[int] = None
    fuel_type: Optional[str] = None
    gearbox: Optional[str] = None
    seats: Optional[int] = None
    description: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True
    )

    @classmethod
    def from_record(cls, record: Record) -> "CarDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            CarDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),  # type: ignore
            brand=record_dict.get("brand"),  # type: ignore
            model=record_dict.get("model"),  # type: ignore
            year=record_dict.get("year"),  # type: ignore
            price_per_day=record_dict.get("price_per_day"),  # type: ignore
            registration_number=record_dict.get("registration_number"),  # type: ignore
            mileage=record_dict.get("mileage"),
            fuel_type=record_dict.get("fuel_type"),
            gearbox=record_dict.get("gearbox"),
            seats=record_dict.get("seats"),
            description=record_dict.get("description")
        )
