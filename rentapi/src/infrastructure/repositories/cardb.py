"""Module containing car repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore

from rentapi.src.core.repositories.icar import ICarRepository
from rentapi.src.core.domain.car import Car, CarIn
from rentapi.src.db import car_table, database
from rentapi.src.infrastructure.dto.cardto import CarDTO


class CarRepository(ICarRepository):
    """A class representing car DB repository."""

    async def get_all_cars(self) -> Iterable[Any]:
        """The abstract getting all cars from the data storage.

        Returns:
            Iterable[Any]: Cars in the data storage
        """

        query = car_table.select()

        cars = await database.fetch_all(query)

        return [CarDTO.from_record(car) for car in cars]

    async def get_car_by_id(self, car_id: int) -> Any | None:
        """The abstract getting car provided id.

        Args:
            car_id (int): The id of the car.

        Returns:
            Any | None: The car details.
        """

        query = car_table.select().where(car_table.c.id == car_id)

        car = await database.fetch_one(query)

        return CarDTO.from_record(car) if car else None

    async def get_car_by_brand(self, name: str) -> Iterable[Any]:
        """The abstract getting car provided by brand.

        Args:
            name (str): The name of the car brand.

        Returns:
            Iterable[Any]: The car details associated with the car model.
        """

        query = car_table.select().where(
            car_table.c.brand.ilike(f"%{name}%")
        )

        cars = await database.fetch_all(query)

        return [CarDTO.from_record(car) for car in cars]

    async def get_car_by_model(self, name: str) -> Iterable[Any]:
        """The method getting cars provided by model.

        Args:
            name (str): The name of the car model.

        Returns:
            Iterable[CarDTO]: The cars details.
        """

        query = car_table.select().where(
            car_table.c.model.ilike(f"%{name}%")
        )

        cars = await database.fetch_all(query)

        return [CarDTO.from_record(car) for car in cars]

    async def add_car(self, data: CarIn) -> Any | None:
        """The abstract adding new car to the data storage.

        Args:
            data (CarIn): The details of the new car.

        Returns:
            Any | None: The newly added car.
        """

        query = car_table.insert().values(**data.model_dump())
        new_car_id = await database.execute(query)
        new_car = await self._get_by_id(new_car_id)

        return Car(**dict(new_car)) if new_car else None

    async def update_car(
            self,
            car_id: int,
            data: CarIn
    ) -> Any | None:
        """The abstract updating car data in the data storage.

        Args:
            car_id (int): The id of the car
            data (CarIn): The details of the update car.

        Returns:
            Any | None: The updated car details.
        """

        if self._get_by_id(car_id):
            query = (
                car_table.update()
                .where(car_table.c.id == car_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            car = await self._get_by_id(car_id)

            return Car(**dict(car)) if car else None

    async def delete_car(self, car_id: int) -> bool:
        """The abstract removing car from the data storage.

        Args:
             car_id (int): The id of the car.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(car_id):
            query = car_table \
                .delete() \
                .where(car_table.c.id == car_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, car_id: int) -> Record | None:
        """A private method getting car from the DB based on its ID.

        Args:
            car_id (int): The ID of the car.

        Returns:
            Any | None: car record if exists.
        """

        query = (
            car_table.select()
            .where(car_table.c.id == car_id)
        )

        return await database.fetch_one(query)
