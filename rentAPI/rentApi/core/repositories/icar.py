"""Module containing car repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from rentApi.core.domain.car import CarIn


class ICarRepository(ABC):
    """An abstract class representing protocol of continent repository."""

    @abstractmethod
    async def get_cars(self) -> Iterable[Any]:
        """The abstract getting all cars from the data storage.

        Returns:
            Iterable[Any]: Cars in the data storage
        """

    @abstractmethod
    async def get_car_by_id(self, car_id: int) -> Any | None:
        """The abstract getting car provided id.

        Args:
            car_id (int): The id of the car.

        Returns:
            Any | None: The car details.
        """

    @abstractmethod
    async def get_car_by_model(self, name: str) -> Iterable[Any] | None:
        """The abstract getting car provided id.

        Args:
            name (str): The name of the car model.

        Returns:
            Iterable[Any] | None: The car details associated with the car model.
        """

    @abstractmethod
    async def add_car(self, data: CarIn) -> Any | None:
        """The abstract adding new car to the data storage.

        Args:
            data (CarIn): The details of the new car.

        Returns:
            Any | None: The newly added car.
        """

    @abstractmethod
    async def update_car(
            self,
            car_id: int,
            data: CarIn
    ) -> Any | None:
        """The abstract adding new car to the data storage.

        Args:
            car_id (int): The id of the car
            data (CarIn): The details of the update car.

        Returns:
            Any | None: The updated car details.
        """

    @abstractmethod
    async def delete_car(self, car_id: int) -> bool:
        """The abstract removing car from the data storage.

        Args:
             car_id (int): The id of the car.

        Returns:
            bool: Success of the operation.
        """
