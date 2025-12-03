"""A module containing DTO models for output cars."""

from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict
from rentapi.src.infrastructure.dto.cardto import CarDTO
from rentapi.src.infrastructure.dto.userdto import UserDTO


class ReviewDTO(BaseModel):
    """A model representing DTO for review data."""

    user: UserDTO
    car: CarDTO
    body: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True
    )

    @classmethod
    def from_record(cls, record: Record) -> "ReviewDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            ReviewDTO: The final DTO instance.
        """

        record_dict = dict(record)

        return cls(
            user=UserDTO(),
            car=CarDTO(),
            body=record_dict.get("body")
        )