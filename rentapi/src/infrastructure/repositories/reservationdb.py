"""Module containing reservation repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, and_, or_
from datetime import datetime

from src.core.repositories.ireservation import IReservationRepository
from src.core.domain.reservation import Reservation, ReservationBroker, ReservationStatus
from src.db import (
    reservation_table,
    user_table,
    car_table,
    database
)
from src.infrastructure.dto.reservationdto import ReservationDTO


# noinspection PyTestUnpassedFixture
class ReservationRepository(IReservationRepository):
    """A class representing reservation DB repository."""

    async def get_all_reservations(self) -> Iterable[Any]:
        """The method getting all reservations from the data storage.

        Returns:
            Iterable[Any]: Reservations in the data storage.
        """

        query = (
            select(reservation_table, user_table, car_table)
            .select_from(
                reservation_table
                .join(
                    car_table,
                    reservation_table.c.car_id == car_table.c.id
                )
                .join(
                    user_table,
                    reservation_table.c.user_id == user_table.c.id
                )
            )
            .order_by(reservation_table.c.id.asc())
        )

        reservations = await database.fetch_all(query)

        return [ReservationDTO.from_record(review) for review in reservations]

    async def get_by_id(self, reservation_id: int) -> Any | None:
        """The method getting reservation provided by id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Any | None: The reservation details.
        """

        query = (
            select(reservation_table, user_table, car_table)
            .select_from(
                reservation_table
                .join(
                    car_table,
                    reservation_table.c.car_id == car_table.c.id
                )
                .join(
                    user_table,
                    reservation_table.c.user_id == user_table.c.id
                )
            )
            .where(reservation_table.c.id == reservation_id)
            .order_by(reservation_table.c.id.asc())
        )

        reservation = await database.fetch_one(query)

        return ReservationDTO.from_record(reservation) if reservation else None

    async def get_by_car(self, car_id: int) -> Iterable[Any]:
        """The method getting reservation provided by car id.

        Args:
            car_id (int): The id of the car.

        Returns:
            Any | None: The reservation details.
        """

        query = reservation_table \
            .select() \
            .where(reservation_table.c.car_id == car_id) \
            .order_by(reservation_table.c.id.asc())

        reservations = await database.fetch_all(query)

        return [ReservationDTO.from_record(reservation) for reservation in reservations]

    async def get_by_user(self, user_id: str) -> Iterable[Any]:
        """The method getting all provided user's reservation from the data storage.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Any]: The collection of the reservations.
        """

        query = reservation_table \
            .select() \
            .where(reservation_table.c.user_id == user_id) \
            .order_by(reservation_table.c.id.asc())

        reservations = await database.fetch_all(query)

        return [ReservationDTO.from_record(reservation) for reservation in reservations]

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

        query = (
            reservation_table.select()
            .where(
                and_(
                    reservation_table.c.car_id == car_id,
                    or_(
                        reservation_table.c.reservation_status != "CANCELLED",
                        reservation_table.c.reservation_status.is_(None)
                    ),
                    or_(
                        and_(
                            reservation_table.c.reservation_start >= start_date,
                            reservation_table.c.reservation_start < end_date
                        ),
                        and_(
                            reservation_table.c.reservation_end > start_date,
                            reservation_table.c.reservation_end <= end_date
                        ),
                        and_(
                            reservation_table.c.reservation_start <= start_date,
                            reservation_table.c.reservation_end >= end_date
                        )
                    )
                )
            )
        )

        availability = await database.fetch_all(query)

        return len(availability) == 0

    async def has_completed(
            self,
            user_id: str,
            car_id: int
    ) -> bool:
        """The method checking if user completed the reservation for particular car.

        Args:
            user_id (int): The id of the user.
            car_id (int): The id of the car.

        Returns:
            bool: True if user completed the reservation for particular car.
        """

        query = (
            reservation_table.select()
            .where(
                and_(
                    reservation_table.c.user_id == user_id,
                    reservation_table.c.car_id == car_id,
                    reservation_table.c.reservation_status == "COMPLETED"
                )
            )
        )
        reservation = await database.fetch_one(query)

        return reservation is not None

    async def update_reservation_status(
            self,
            reservation_id: int,
            status: str,
    ) -> Any | None:
        """The method updating reservation status.

        Args:
            reservation_id (int): The reservation id.
            status (str): The new status.

        Returns:
            Any | None: The updated reservation.
        """

        if await self._get_by_id(reservation_id):
            query = (
                reservation_table.update()
                .where(reservation_table.c.id == reservation_id)
                .values(reservation_status=status)
            )
            await database.execute(query)

            reservation = await self._get_by_id(reservation_id)
            if reservation:
                record_dict = dict(reservation)
                record_dict["status"] = record_dict.pop("reservation_status", ReservationStatus.PENDING)
                return Reservation(**record_dict)
            return None

        return None

    async def add_reservation(self, data: ReservationBroker, total_price: float) -> Any | None:
        """The method adding new reservation to the data storage.

        Args:
            data (ReservationIn): The attributes of the reservation.
            total_price (float): The calculated total price of reservation data.

        Returns:
            Any | None: The newly created reservation.
        """

        data_dict = data.model_dump()
        data_dict["total_price"] = total_price
        query = reservation_table.insert().values(**data_dict)
        new_reservation_id = await database.execute(query)
        new_reservation = await self._get_by_id(new_reservation_id)

        return Reservation(**dict(new_reservation)) if new_reservation else None

    async def update_reservation(
            self,
            reservation_id: int,
            data: ReservationBroker,
    ) -> Any | None:
        """The method updating reservation data in the data storage.

        Args:
            reservation_id (int): The reservation id.
            data (ReservationIn): The attributes of the reservation.

        Returns:
            Any | None: The updated reservation.
        """

    async def delete_reservation(self, reservation_id: int) -> bool:
        """The method updating removing reservation from the data storage.

        Args:
            reservation_id (int): The reservation id.

        Returns:
            bool: Success of the operation.
        """

    async def _get_by_id(self, reservation_id: int) -> Record | None:
        """A private method getting reservation from the DB based on its ID.

        Args:
            reservation_id (int): The ID of the reservation.

        Returns:
            Any | None: Reservation record if exists.
        """

        query = (
            reservation_table.select()
            .where(reservation_table.c.id == reservation_id)
            .order_by(reservation_table.c.id.asc())
        )

        return await database.fetch_one(query)
