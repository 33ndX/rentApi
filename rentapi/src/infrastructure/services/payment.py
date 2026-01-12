"""Module containing payment service implementation."""

from typing import Iterable

from src.core.domain.payment import PaymentIn, Payment, PaymentStatus
from src.core.repositories.ipayment import IPaymentRepository
from src.core.repositories.ireservation import IReservationRepository
from src.infrastructure.dto.paymentdto import PaymentDTO
from src.infrastructure.payments.stripe_gateway import StripeGateway
from src.infrastructure.services.ipayment import IPaymentService
from src.core.domain.reservation import ReservationStatus


class PaymentService(IPaymentService):
    """A class implementing the payment service."""

    _repository: IPaymentRepository
    _reservation_repository: IReservationRepository
    _gateway: StripeGateway

    def __init__(
            self,
            repository: IPaymentRepository,
            reservation_repository: IReservationRepository,
            gateway: StripeGateway
    ):
        """The initializer of the `payment service`.

          Args:
              repository (IPaymentRepository): The reference to the repository.
              reservation_repository (IReservationRepository): The reference to the reservation repository.
              gateway (StripeGateway): The reference to the Stripe gateway.
          """

        self._repository = repository
        self._reservation_repository = reservation_repository
        self._gateway = gateway

    async def get_payments(self) -> Iterable[PaymentDTO]:
        """The method getting all payments from the repository.

        Returns:
            Iterable[PaymentDTO]: All payments.
        """

        return await self._repository.get_payments()

    async def get_by_user(self, user_id: str) -> Iterable[PaymentDTO]:
        """The method getting payments assigned to particular user.

        Args:
            user_id (str): The id of the user.

        Returns:
            PaymentDTO: Payments assigned to a user.
        """

        return await self._repository.get_by_user(user_id)

    async def get_by_reservation(self, reservation_id: int) -> PaymentDTO | None:
        """The method getting payment assigned to particular reservation.

        Args:
             reservation_id (int): The id of the reservation.

        Returns:
            PaymentDTO | None: Reservation assigned to a car.
        """

        return await self._repository.get_by_reservation(reservation_id)

    async def process_payment(self, reservation_id: int, user_id: str) -> Payment | None:
        """The abstract processing payment for a reservation.

        Args:
            reservation_id (int): The id of the reservation.
            user_id (str): The id of the user.

        Returns:
            Payment | None: The processed payment details.
        """

        reservation = await self._reservation_repository.get_by_id(reservation_id)

        if not reservation:
            raise ValueError("Reservation not found")

        if str(reservation.user_id) != user_id:
            raise ValueError("You can only pay for your own reservations")

        status = reservation.status

        if status != ReservationStatus.PENDING:
            raise ValueError("Reservation already paid or cancelled")

        is_paid = await self._repository.get_by_reservation(reservation_id)
        if is_paid and is_paid.status == PaymentStatus.PAID:
            return None

        intent = await self._gateway.create_payment_intent(
            amount=reservation.total_price,
            currency="pln"
        )

        if not intent:
            raise ValueError("Can't creat payment intent")

        payment_creation = PaymentIn(
            reservation_id=reservation_id,
            amount=reservation.total_price
        )

        payment = await self._repository.add_payment(payment_creation)

        if not payment:
            raise ValueError("Can't creat payment")

        charge_confirmed = await self._gateway.confirm_payment(intent.id)

        if not charge_confirmed:
            await self._repository.update_payment_status(
                payment_id=payment.id,
                status=PaymentStatus.FAILED.value
            )
            raise ValueError("Failed to confirm payment via Stripe")

        updated_payment = await self._repository.update_payment_status(
            payment_id=payment.id,
            status=PaymentStatus.PAID.value
        )

        await self._reservation_repository.update_reservation_status(
            reservation_id=reservation_id,
            status=ReservationStatus.CONFIRMED.value
        )

        return updated_payment
