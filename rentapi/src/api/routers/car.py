"""A module containing car endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from src.infrastructure.utils import consts
from src.container import Container
from src.core.domain.car import Car, CarIn
from src.infrastructure.dto.cardto import CarDTO
from src.infrastructure.services.icar import ICarService

router = APIRouter()

@router.post("/create", response_model=Car, status_code=201)
@inject
async def create_car(
      car: CarIn,
      service: ICarService = Depends(Provide[Container.car_service]),
) -> dict:
    """An endpoint for adding new car.

    Args:
        car (CarIn): The car data.
        service (ICarService, optional): The injected service dependency.

    Returns:
        dict: The new car attributes.
    """

    new_car = await service.add_car(car)

    return new_car.model_dump() if new_car else {}

@router.get("/all", response_model=Iterable[Car], status_code=200)
@inject
async def get_all_cars(
        service: ICarService = Depends(Provide[Container.car_service]),
) -> Iterable:
    """An endpoint for getting all cars.

    Args:
        service (ICarService, optional): The injected service dependency.

    Returns:
        Iterable: The car attributes collection.
    """

    cars = await service.get_cars()

    return cars

@router.get("/{car_id}", response_model=Car, status_code=200)
@inject
async def get_car_by_id(
        car_id: int,
        service: ICarService = Depends(Provide[Container.car_service]),
) -> dict:
    """An endpoint for getting car details by id.

    Args:
        car_id (int): The id of the car.
        service (ICarService): The injected service dependency.

    Raises:
        HTTPException: 404 if car does not exist.

    Returns:
        dict: The requested car attributes.
    """

    if car := await service.get_car_by_id(car_id):
        return car.model_dump()

    raise HTTPException(status_code=404, detail="car not found")

@router.put("/{car_id}", response_model=Car, status_code=201)
@inject
async def update_car(
        car_id: int,
        updated_car: CarIn,
        service: ICarService = Depends(Provide[Container.car_service]),
) -> dict:
    """An endpoint for updating car data.

    Args:
        car_id (int): The id of the car.
        updated_car (CarIn): The updated continent details.
        service (ICarService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if car does not exist.

    Returns:
        dict: The updated car details.
    """

    if await service.get_car_by_id(car_id=car_id):
        new_updated_car = await service.update_car(
            car_id=car_id,
            data=updated_car,
        )
        return new_updated_car.model_dump() if new_updated_car \
            else {}

    raise HTTPException(status_code=404, detail="car not found")

@router.delete("/{car_id}", status_code=204)
@inject
async def delete_car(
        car_id: int,
        service: ICarService = Depends(Provide[Container.car_service]),
) -> None:
    """An endpoint for deleting cars.

    Args:
        car_id (int): The id of the continent.
        service (ICarService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if car does not exist.

    Returns:
        dict: Empty if operation finished.
    """

    if await service.get_car_by_id(car_id=car_id):
        await service.delete_car(car_id)
        return

    raise HTTPException(status_code=404, detail="car not found")

