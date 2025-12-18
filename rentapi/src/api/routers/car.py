"""A module containing car endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from rentapi.src.infrastructure.utils import consts
from rentapi.src.container import Container
from rentapi.src.core.domain.car import Car, CarIn
from rentapi.src.infrastructure.dto.cardto import CarDTO
from rentapi.src.infrastructure.services.icar import ICarService

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



