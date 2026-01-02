"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from src.infrastructure.repositories.cardb import \
    CarRepository
from src.infrastructure.repositories.userdb import \
    UserRepository

from src.infrastructure.services.car import CarService
from src.infrastructure.services.user import UserService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    car_repository = Singleton(CarRepository)
    user_repository = Singleton(UserRepository)

    car_service = Factory(
        CarService,
        repository=car_repository
    )

    user_service = Factory(
        UserService,
        repository=user_repository
    )
