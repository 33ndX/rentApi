"""Module containing car service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.car import Car, CarIn
from src.infrastructure.dto.cardto import CarDTO


class ICarService(ABC):
    """A class representing a car repository."""

    @abstractmethod
    async def get_cars(self) -> Iterable[CarDTO]:
        """The method getting all cars from the repository.

        Returns:
            Iterable[CarDTO]: All cars.
        """

    @abstractmethod
    async def get_car_by_id(self, car_id: int) -> CarDTO | None:
        """The method getting car by provided id.

        Args:
            car_id (int): The id of the car.

        Returns:
            CarDTO | None: The car details.
        """

    @abstractmethod
    async def get_car_by_brand(self, name: str) -> Iterable[Car]:
        """The method getting cars provided by brand.

        Args:
            name (str): The name of the car brand.

        Returns:
            Iterable[CarDTO]: The cars details.
        """
    @abstractmethod
    async def get_car_by_model(self, name: str) -> Iterable[Car]:
        """The method getting cars provided by model.

        Args:
            name (str): The name of the car model.

        Returns:
            Iterable[CarDTO]: The cars details.
        """

    @abstractmethod
    async def add_car(self, data: CarIn) -> Car | None:
        """The method adding new car to the data storage.

        Args:
            data (CarIn): The details of the new car.

        Returns:
            Car | None: Full details of the newly added car.
        """

    @abstractmethod
    async def update_car(
            self,
            car_id: int,
            data: CarIn
    ) -> Car | None:
        """The method updating car data in the data storage.

        Args:
            car_id (int): The id of the car.
            data (CarIn): The details of the updated car.

        Returns:
            Car | None: The updated car details.
        """

    @abstractmethod
    async def delete_car(self, car_id: int) -> bool:
        """The method updating removing car from the data storage.

        Args:
            car_id (int): The id of the car.

        Returns:
            bool: Success of the operation.
        """