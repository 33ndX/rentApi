"""Module containing reservation service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from pydantic import UUID1

from src.core.domain.reservation import Reservation, ReservationBroker
from src.infrastructure.dto.reservationdto import ReservationDTO



class IReservationService(ABC):
    """A class representing reservation repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[ReservationDTO]:
        """The method getting all reservation from the repository.

        Returns:
            Iterable[ReservationDTO]: All reservations.
        """

    @abstractmethod
    async def get_by_car(self, car_id: int) -> ReservationDTO:
        """The method getting reservations assigned to particular car.

        Args:
            car_id (int): The id of the car.

        Returns:
            ReservationDTO: Reservation assigned to a car.
        """

    @abstractmethod
    async def get_by_id(self, reservation_id: int) -> ReservationDTO:
        """The method getting reservations assigned to particular id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            ReservationDTO: Reservation assigned to an id.
        """

    @abstractmethod
    async def get_by_user(self, user_id: UUID1) -> Iterable[ReservationDTO]:
        """The method getting reservations assigned to particular user.

        Args:
            user_id (UUID1): The id of the user.

        Returns:
            ReservationDTO: Reservation assigned to a user.
        """

    @abstractmethod
    async def add_reservation(self, data: ReservationBroker) -> Reservation | None :
        """The method adding new reservation to the data storage.

        Args:
            data (ReservationBroker): The details of the new reservation.

        Returns:
            Reservation | None: Full details of the newly added reservation.
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
