"""Module containing payment repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from src.core.domain.payment import PaymentIn


class IPaymentRepository(ABC):
    """An abstract class representing protocol of payment repository."""

    @abstractmethod
    async def get_payments(self) -> Iterable[Any]:
        """The abstract getting all payments from the data storage.

        Returns:
            Iterable[Any]: Payments in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, payment_id: int) -> Any | None:
        """The abstract getting payment provided by id.

        Args:
            payment_id (int): The id of the payment.

        Returns:
            Any | None: The payment details.
        """

    @abstractmethod
    async def get_by_user(self, user_id: str) -> Iterable[Any]:
        """The abstract getting all provided user's payment from the data storage.

        Args:
            user_id (str): The id of the user.

        Returns:
            Iterable[Any]: The collection of the payments.
        """

    @abstractmethod
    async def get_by_reservation(self, reservation_id: int) -> Any | None:
        """The abstract getting payment provided by reservation id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Any | None: The payment details.
        """
    @abstractmethod
    async def add_payment(self, data: PaymentIn) -> Any | None:
        """The abstract adding new payment to the data storage.

        Args:
            data (PaymentIn): The attributes of the payment.

        Returns:
            Any | None: The newly created payment.
        """

    @abstractmethod
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