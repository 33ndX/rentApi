"""Modul containing car-related domain models."""

from typing import Optional

from pydantic import BaseModel, ConfigDict


class CarIn(BaseModel):
    """Model representing car's attributes."""
    brand: str
    model: str
    year: int
    price_per_day: float
    registration_number: str
    mileage: Optional[int]
    fuel_type: Optional[str]
    gearbox: Optional[str]
    seats: Optional[int]
    description: Optional[str]


class Car(CarIn):
    """Model representing car's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
