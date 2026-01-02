"""Module containing reservation repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from pydantic import UUID1

from src.core.domain.reservation import ReservationIn


class IReservationRepository(ABC):
    """An abstract class representing protocol of reservation repository."""

    @abstractmethod
    async def get_reservations(self) -> Iterable[Any]:
        """The abstract getting all reservations from the data storage.

        Returns:
            Iterable[Any]: Reservations in the data storage.
        """

    @abstractmethod
    async def get_by_car(self, car_id: int) -> Iterable[Any]:
        """The abstract getting reservation provided by car id.

        Args:
            car_id (int): The id of the car.

        Returns:
            Any | None: The reservation details.
        """

    @abstractmethod
    async def get_by_id(self, reservation_id: int) -> Any:
        """The abstract getting reservation provided by id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Any | None: The reservation details.
        """

    @abstractmethod
    async def get_by_user(self,
                          user_id: UUID1
                          ) -> Iterable[Any]:
        """The abstract getting all provided user's reservation
            from the data storage.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Any]: The collection of the reservations.
        """

    @abstractmethod
    async def add_reservation(self, data: ReservationIn) -> Any | None:
        """The abstract adding new reservation to the data storage.

        Args:
            data (ReservationIn): The attributes of the reservation.

        Returns:
            Any | None: The newly created reservation.
        """

    @abstractmethod
    async def update_reservation(
        self,
        reservation_id: int,
        data: ReservationIn,
    ) -> Any | None:
        """The abstract updating reservation data in the data storage.

        Args:
            reservation_id (int): The reservation id.
            data (ReservationIn): The attributes of the reservation.

        Returns:
            Any | None: The updated reservation.
        """

    @abstractmethod
    async def delete_reservation(self, reservation_id: int) -> bool:
        """The abstract updating removing reservation from the data storage.

        Args:
            reservation_id (int): The reservation id.

        Returns:
            bool: Success of the operation.
        """



