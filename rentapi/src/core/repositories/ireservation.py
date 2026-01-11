"""Module containing reservation repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable
from datetime import datetime

from pydantic import UUID1

from src.core.domain.reservation import ReservationIn


class IReservationRepository(ABC):
    """An abstract class representing protocol of reservation repository."""

    @abstractmethod
    async def get_all_reservations(self) -> Iterable[Any]:
        """The abstract getting all reservations from the data storage.

        Returns:
            Iterable[Any]: Reservations in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, reservation_id: int) -> Any | None:
        """The abstract getting reservation provided by id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Any | None: The reservation details.
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
    async def get_by_user(self, user_id: str) -> Iterable[Any]:
        """The abstract getting all provided user's reservation from the data storage.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Any]: The collection of the reservations.
        """

    @abstractmethod
    async def check_car_availability(
            self,
            car_id: int,
            start_date: datetime,
            end_date: datetime
    ) -> bool:
        """The method checking if car is available for the given period

        Args:
            car_id (int): The id of the car.
            start_date (datetime): Start of the period.
            end_date (datetime): End of the period.

        Returns:
            bool: True if car is available.
        """

    @abstractmethod
    async def has_completed(
            self,
            user_id: UUID1,
            car_id: int
    ) -> bool:
        """The method checking if user completed the reservation for particular car.

        Args:
            user_id (int): The id of the user.
            car_id (int): The id of the car.

        Returns:
            bool: True if user completed the reservation for particular car.
        """

    @abstractmethod
    async def update_reservation_status(
            self,
            reservation_id: int,
            status: str,
    ) -> Any | None:
        """The abstract updating reservation status.

        Args:
            reservation_id (int): The reservation id.
            status (str): The new status.

        Returns:
            Any | None: The updated reservation.
        """

    @abstractmethod
    async def add_reservation(self, data: ReservationIn, total_price: float) -> Any | None:
        """The abstract adding new reservation to the data storage.

        Args:
            data (ReservationIn): The attributes of the reservation.
            total_price (float): The calculated total price of reservation data.

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
