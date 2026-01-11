"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from src.infrastructure.payments.stripe_gateway import StripeGateway
from src.infrastructure.repositories.cardb import \
    CarRepository
from src.infrastructure.repositories.userdb import \
    UserRepository
from src.infrastructure.repositories.reviewdb import \
    ReviewRepository
from src.infrastructure.repositories.reservationdb import \
    ReservationRepository
from src.infrastructure.repositories.paymentdb import \
    PaymentRepository

from src.infrastructure.services.car import CarService
from src.infrastructure.services.review import ReviewService
from src.infrastructure.services.user import UserService
from src.infrastructure.services.reservation import ReservationService
from src.infrastructure.services.payment import PaymentService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    car_repository = Singleton(CarRepository)
    reservation_repository = Singleton(ReservationRepository)
    review_repository = Singleton(ReviewRepository)
    user_repository = Singleton(UserRepository)
    payment_repository = Singleton(PaymentRepository)
    stripe_gateway = Singleton(StripeGateway)

    car_service = Factory(
        CarService,
        repository=car_repository
    )

    reservation_service = Factory(
        ReservationService,
        repository=reservation_repository,
        car_repository=car_repository
    )

    review_service = Factory(
        ReviewService,
        repository=review_repository,
        reservation_repository=reservation_repository
    )

    payment_service = Factory(
        PaymentService,
        repository=payment_repository,
        reservation_repository=reservation_repository,
        gateway=stripe_gateway
    )

    user_service = Factory(
        UserService,
        repository=user_repository
    )
