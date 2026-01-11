"""Module containing payment repository abstractions."""

from typing import Any, Iterable
from asyncpg import Record  # type: ignore
from sqlalchemy import select

from src.core.repositories.ipayment import IPaymentRepository
from src.core.domain.payment import Payment, PaymentIn
from src.db import (
    payment_table,
    reservation_table,
    user_table,
    database
)
from src.infrastructure.dto.paymentdto import PaymentDTO


class PaymentRepository(IPaymentRepository):
    """An abstract class representing protocol of payment repository."""

    async def get_payments(self) -> Iterable[Any]:
        """The abstract getting all payments from the data storage.

        Returns:
            Iterable[Any]: Payments in the data storage.
        """

        query = (
            select(payment_table, reservation_table, user_table)
            .select_from(
                payment_table
                .join(
                    reservation_table,
                    payment_table.c.reservation_id == reservation_table.c.id
                )
                .join(
                    user_table,
                    payment_table.c.user_id == user_table.c.id
                )
            )
            .order_by(payment_table.c.id.asc())
        )

        payments = await database.fetch_all(query)

        return [PaymentDTO.from_record(payment) for payment in payments]

    async def get_by_id(self, payment_id: int) -> Any | None:
        """The abstract getting payment provided by id.

        Args:
            payment_id (int): The id of the payment.

        Returns:
            Any | None: The payment details.
        """

        query = (
            select(payment_table, reservation_table, user_table)
            .select_from(
                payment_table
                .join(
                    reservation_table,
                    payment_table.c.reservation_id == reservation_table.c.id
                )
                .join(
                    user_table,
                    payment_table.c.user_id == user_table.c.id
                )
            )
            .where(payment_table.c.id == payment_id)
            .order_by(payment_table.c.id.asc())
        )

        payment = await database.fetch_all(query)

        return PaymentDTO.from_record(payment) if payment else None

    async def get_by_user(self, user_id: str) -> Iterable[Any]:
        """The abstract getting all provided user's payment from the data storage.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Any]: The collection of the payments.
        """

        query = payment_table \
            .select() \
            .where(payment_table.c.user_id == user_id) \
            .order_by(payment_table.c.id.asc())

        payments = await database.fetch_all(query)

        return [PaymentDTO.from_record(payment) for payment in payments]

    async def get_by_reservation(self, reservation_id: int) -> Any | None:
        """The abstract getting payment provided by reservation id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Any | None: The payment details.
        """

        query = payment_table \
            .select() \
            .where(payment_table.c.reservation_id == reservation_id) \
            .order_by(payment_table.c.id.asc())

        payment = await database.fetch_one(query)

        return Payment(**dict(payment)) if payment else None

    async def add_payment(self, data: PaymentIn) -> Any | None:
        """The abstract adding new payment to the data storage.

        Args:
            data (PaymentIn): The attributes of the payment.

        Returns:
            Any | None: The newly created payment.
        """

        query = payment_table.insert().values(**data.model_dump())
        new_payment_id = await database.execute(query)
        new_payment = await self._get_by_id(new_payment_id)

        if not new_payment:
            return None

        res_dict = dict(new_payment)
        if res_dict.get("status") is None:
            res_dict["status"] = "PENDING"

        return Payment(**res_dict)

    async def update_payment_status(
        self,
        payment_id: int,
        status: str,
    ) -> Any | None:
        """The abstract updating payment status.

        Args:
            payment_id (int): The payment id.
            status (str): The new status.

        Returns:
            Any | None: The updated payment.
        """

        if await self._get_by_id(payment_id):
            query = (
                payment_table.update()
                .where(payment_table.c.id == payment_id)
                .values(status=status)
            )
            await database.execute(query)

            payment = await self._get_by_id(payment_id)

            return Payment(**dict(payment)) if payment else None

        return None

    async def _get_by_id(self, payment_id: int) -> Record | None:
        """A private method getting payment from the DB based on its ID.

        Args:
            payment_id (int): The ID of the payment.

        Returns:
            Any | None: Payment record if exists.
        """

        query = (
            payment_table.select()
            .where(payment_table.c.id == payment_id)
        )

        return await database.fetch_one(query)
