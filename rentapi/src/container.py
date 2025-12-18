"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from rentapi.src.infrastructure.repositories.cardb import \
    CarRepository

from rentapi.src.infrastructure.services.car import CarService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    car_repository = Singleton(CarRepository)

    car_service = Factory(
        CarService,
        repository=car_repository
    )
