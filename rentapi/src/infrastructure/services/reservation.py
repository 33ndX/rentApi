"""Module containing reservation service implementation."""

from typing import Iterable
from datetime import datetime

from src.core.domain.reservation import Reservation, ReservationBroker, ReservationStatus
from src.core.repositories.icar import ICarRepository
from src.core.repositories.ireservation import IReservationRepository
from src.infrastructure.dto.reservationdto import ReservationDTO
from src.infrastructure.services.ireservation import IReservationService


class ReservationService(IReservationService):
    """A class implementing the reservation service."""

    _repository: IReservationRepository
    _car_repository: ICarRepository

    def __init__(
            self,
            repository: IReservationRepository,
            car_repository: ICarRepository
    ):
        """The initializer of the `reservation service`.

        Args:
            repository (IReservationRepository): The reference to the repository.
            car_repository (ICarRepository): The reference to the reservation repository.
        """

        self._repository = repository
        self._car_repository = car_repository

    async def get_reservations(self) -> Iterable[ReservationDTO]:
        """The method getting all reservation from the repository.

        Returns:
            Iterable[ReservationDTO]: All reservations.
        """

        return await self._repository.get_all_reservations()

    async def get_by_id(self, reservation_id: int) -> ReservationDTO | None:
        """The method getting reservations assigned to particular id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            ReservationDTO: Reservation assigned to an id.
        """

        return await self._repository.get_by_id(reservation_id)

    async def get_by_car(self, car_id: int) -> Iterable[ReservationDTO]:
        """The method getting reservations assigned to particular car.

        Args:
            car_id (int): The id of the car.

        Returns:
            ReservationDTO: Reservation assigned to a car.
        """

        return await self._repository.get_by_car(car_id)

    async def get_by_user(self, user_id: str) -> Iterable[ReservationDTO]:
        """The method getting reservations assigned to particular user.

        Args:
            user_id (UUID1): The id of the user.

        Returns:
            ReservationDTO: Reservation assigned to a user.
        """

        return await self._repository.get_by_user(user_id)

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

        return await self._repository.check_car_availability(car_id, start_date, end_date)

    async def add_reservation(self, data: ReservationBroker) -> Reservation | None:
        """The method adding new reservation to the data storage.

        Args:
            data (ReservationBroker): The details of the new reservation.

        Returns:
            Reservation | None: Full details of the newly added reservation.
        """

        car = await self._car_repository.get_car_by_id(data.car_id)
        if car is None:
            raise ValueError("Car not found")

        is_available = await self._repository.check_car_availability(
            car_id=data.car_id,
            start_date=data.reservation_start,
            end_date=data.reservation_end
        )

        if not is_available:
            raise ValueError("Car is not available for the selected period")

        days = (data.reservation_end - data.reservation_start).days
        if days <= 0:
            days = 1
        total_price = car.price_per_day * days

        return await self._repository.add_reservation(
            data=data,
            total_price=total_price,
        )

    async def confirm_reservation(
            self,
            reservation_id: int
    ) -> ReservationDTO | None:
        """The method confirming a reservation.

        Args:
            reservation_id (int): The reservation id.

        Returns:
            ReservationDTO | None: The updated reservation.
        """

        reservation = await self._repository.get_by_id(reservation_id)

        if reservation.status != ReservationStatus.PENDING:
            raise ValueError("Only pending reservations can be confirmed")

        return await self._repository.update_reservation_status(
            reservation_id=reservation_id,
            status=ReservationStatus.CONFIRMED.value,
        )

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

        reservation = await self._repository.get_by_id(reservation_id)

        if reservation.status != ReservationStatus.CONFIRMED:
            raise ValueError("Only confirmed reservations can be started")

        return await self._repository.update_reservation_status(
            reservation_id=reservation_id,
            status=ReservationStatus.IN_PROGRESS.value,
        )

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

        reservation = await self._repository.get_by_id(reservation_id)

        if reservation.status != ReservationStatus.IN_PROGRESS:
            raise ValueError("Only in-progress reservations can be completed")

        return await self._repository.update_reservation_status(
            reservation_id=reservation_id,
            status=ReservationStatus.COMPLETED.value,
        )

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

        reservation = await self._repository.get_by_id(reservation_id)

        if reservation.status in [
            ReservationStatus.CONFIRMED,
            ReservationStatus.IN_PROGRESS,
            ReservationStatus.COMPLETED,
            ReservationStatus.CANCELLED
        ]:
            raise ValueError("Cannot cancel confirmed, in-progress, completed or already cancelled reservations")

        return await self._repository.update_reservation_status(
            reservation_id=reservation_id,
            status=ReservationStatus.CANCELLED.value,
        )

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

        return await self._repository.update_reservation(
            reservation_id=reservation_id,
            data=data
        )

    async def delete_reservation(self, reservation_id: int) -> bool:
        """The method updating removing reservation from the data storage.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_reservation(reservation_id)
