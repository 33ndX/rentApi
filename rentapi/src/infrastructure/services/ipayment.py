"""Module containing payment service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.payment import Payment
from src.infrastructure.dto.paymentdto import PaymentDTO


class IPaymentService(ABC):
    """An abstract class representing protocol of payment service."""

    @abstractmethod
    async def get_payments(self) -> Iterable[PaymentDTO]:
        """The method getting all payments from the repository.

        Returns:
            Iterable[PaymentDTO]: All payments.
        """

    @abstractmethod
    async def get_by_user(self, user_id: str) -> Iterable[PaymentDTO]:
        """The method getting payments assigned to particular user.

        Args:
            user_id (str): The id of the user.

        Returns:
            PaymentDTO: Payments assigned to a user.
        """

    @abstractmethod
    async def get_by_reservation(self, reservation_id: int) -> PaymentDTO | None:
        """The method getting payment assigned to particular reservation.

        Args:
             reservation_id (int): The id of the reservation.

        Returns:
            PaymentDTO | None: Reservation assigned to a car.
        """

    @abstractmethod
    async def process_payment(self, reservation_id: int) -> Payment | None:
        """The abstract processing payment for a reservation.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Payment | None: The processed payment details.
        """
