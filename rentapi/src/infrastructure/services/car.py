"""Module containing car service implementation."""

from typing import Iterable

from rentapi.src.core.domain.car import Car, CarIn
from rentapi.src.core.repositories.icar import ICarRepository
from rentapi.src.infrastructure.dto.cardto import CarDTO
from rentapi.src.infrastructure.services.icar import ICarService


class CarService(ICarService):
    """A class implementing the car service."""

    _repository: ICarRepository

    def __init__(self, repository: ICarRepository):
        """The initializer of the `car service`.

        Args:
            repository (ICarRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_cars(self) -> Iterable[CarDTO]:
        """The method getting all cars from the repository.

        Returns:
            Iterable[CarDTO]: All cars.
        """

        return await self._repository.get_all_cars()

    async def get_car_by_id(self, car_id: int) -> CarDTO | None:
        """The method getting car provided by id.

        Args:
            car_id (int): The id of the car.

        Returns:
            CarDTO | None: The car details.
        """

        return await self._repository.get_car_by_id(car_id)

    async def get_car_by_brand(self, name: str) -> Iterable[Car]:
        """The method getting cars provided by brand.

        Args:
            name (str): The name of the car brand.

        Returns:
            Iterable[CarDTO]: The cars details.
        """

        return await self._repository.get_car_by_brand(name)

    async def get_car_by_model(self, name: str) -> Iterable[Car]:
        """The method getting cars provided by model.

        Args:
            name (str): The name of the car model.

        Returns:
            Iterable[CarDTO]: The cars details.
        """

        return await self._repository.get_car_by_model(name)

    async def add_car(self, data: Car) -> None:
        """The abstract adding new car to the data storage.

        Args:
            data (CarIn): The details of the new car.

        Returns:
            Any | None: The newly added car.
        """

        return await self._repository.add_car(data)

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

        return await self._repository.update_car(
            car_id=car_id,
            data=data
        )

    async def delete_car(self, car_id: int) -> bool:
        """The method updating removing car from the data storage.

        Args:
            car_id (int): The id of the car.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_car(car_id)
