"""Module containing reservation service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from datetime import datetime

from src.core.domain.reservation import Reservation, ReservationBroker
from src.infrastructure.dto.reservationdto import ReservationDTO


class IReservationService(ABC):
    """An abstract class representing protocol of reservation service."""

    @abstractmethod
    async def get_reservations(self) -> Iterable[ReservationDTO]:
        """The method getting all reservation from the repository.

        Returns:
            Iterable[ReservationDTO]: All reservations.
        """

    @abstractmethod
    async def get_by_id(self, reservation_id: int) -> ReservationDTO | None:
        """The method getting reservations assigned to particular id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            ReservationDTO: Reservation assigned to an id.
        """

    @abstractmethod
    async def get_by_car(self, car_id: int) -> Iterable[ReservationDTO]:
        """The method getting reservations assigned to particular car.

        Args:
            car_id (int): The id of the car.

        Returns:
            Iterable[ReservationDTO]: Reservations assigned to a car.
        """

    @abstractmethod
    async def get_by_user(self, user_id: str) -> Iterable[ReservationDTO]:
        """The method getting reservations assigned to particular user.

        Args:
            user_id (str): The id of the user.

        Returns:
            Iterable[ReservationDTO]: Reservations assigned to a user.
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
    async def add_reservation(self, data: ReservationBroker) -> Reservation | None:
        """The method adding new reservation to the data storage.

        Args:
            data (ReservationBroker): The details of the new reservation.

        Returns:
            Reservation | None: Full details of the newly added reservation.
        """

    @abstractmethod
    async def confirm_reservation(
            self,
            reservation_id: int
    ) -> ReservationDTO | None:
        """The method confirming a reservation (typically after payment).

        Args:
            reservation_id (int): The reservation id.

        Returns:
            ReservationDTO | None: The updated reservation.
        """

    @abstractmethod
    async def start_reservation(
            self,
            reservation_id: int
    ) -> ReservationDTO | None:
        """The method marking reservation as in progress.

        Args:
            reservation_id (int): The reservation id.

        Returns:
            ReservationDTO | None: The updated reservation.
        """

    @abstractmethod
    async def complete_reservation(
            self,
            reservation_id: int
    ) -> ReservationDTO | None:
        """The method marking reservation as completed.

        Args:
            reservation_id (int): The reservation id.

        Returns:
            ReservationDTO | None: The updated reservation.
        """

    @abstractmethod
    async def cancel_reservation(
            self,
            reservation_id: int
    ) -> ReservationDTO | None:
        """The method cancelling a reservation.

        Args:
            reservation_id (int): The reservation id.

        Returns:
            ReservationDTO | None: The updated reservation.
        """

    @abstractmethod
    async def update_reservation(
         self,
         reservation_id: int,
         data: ReservationBroker
    ) -> Reservation | None:
        """The method updating reservation data in the data storage.

        Args:
            reservation_id (int): The id of the reservation.
            data (ReservationBroker): The details of the updated reservation.

        Returns:
            Reservation | None: The updated reservation details.
        """

    @abstractmethod
    async def delete_reservation(self, reservation_id: int) -> bool:
        """The method updating removing reservation from the data storage.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            bool: Success of the operation.
        """
