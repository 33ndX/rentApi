"""A module containing reservation endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.infrastructure.utils import consts
from src.container import Container
from src.core.domain.reservation import ReservationIn, ReservationBroker
from src.infrastructure.dto.reservationdto import ReservationDTO
from src.infrastructure.services.ireservation import IReservationService

bearer_scheme = HTTPBearer()

router = APIRouter()


@router.post("/create", response_model=ReservationDTO, status_code=201)
@inject
async def create_reservation(
    reservation: ReservationIn,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new reservation.

    Args:
        reservation (ReservationIn): The reservation data.
        service (IReservationService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The new reservation attributes.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    try:
        extended_reservation_data = ReservationBroker(
            user_id=user_uuid,
            **reservation.model_dump(),
        )
        new_reservation = await service.add_reservation(extended_reservation_data)

        return new_reservation.model_dump() if new_reservation else {}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all", response_model=Iterable[ReservationDTO], status_code=200)
@inject
async def get_all_reservations(
    service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> Iterable:
    """An endpoint for getting all reservations.

    Args:
        service (IReservationService, optional): The injected service dependency.

    Returns:
        Iterable: The reservation attributes collection.
    """

    reservations = await service.get_reservations()

    return reservations


@router.get(
    "/my",
    response_model=Iterable[ReservationDTO],
    status_code=200,
)
@inject
async def get_my_reservations(
    service: IReservationService = Depends(Provide[Container.reservation_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Iterable:
    """An endpoint for getting the current user's reservations.

    Args:
        service (IReservationService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        Iterable: The reservation details collection.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    reservations = await service.get_by_user(user_uuid)

    return reservations


@router.get(
        "/{reservation_id}",
        response_model=ReservationDTO,
        status_code=200,
)
@inject
async def get_reservation_by_id(
    reservation_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> dict | None:
    """An endpoint for getting reservation by id.

    Args:
        reservation_id (int): The id of the reservation.
        service (IReservationService, optional): The injected service dependency.

    Returns:
        dict | None: The reservation details.
    """

    if reservation := await service.get_by_id(reservation_id):
        return reservation.model_dump()

    raise HTTPException(status_code=404, detail="Reservation not found")


@router.put(
        "/cancel/{reservation_id}",
        response_model=ReservationDTO,
        status_code=200,
)
@inject
async def cancel_reservation(
    reservation_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for cancelling reservation.

    Args:
        reservation_id (int): The id of the reservation.
        service (IReservationService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The cancelled reservation details.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if reservation := await service.get_by_id(reservation_id):
        if str(reservation.user_id) != user_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")

        try:
            cancelled_reservation = await service.cancel_reservation(reservation_id)
            return cancelled_reservation.model_dump() if cancelled_reservation else {}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    raise HTTPException(status_code=404, detail="Reservation not found")


@router.put(
        "/start/{reservation_id}",
        response_model=ReservationDTO,
        status_code=200,
)
@inject
async def start_reservation(
    reservation_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for starting reservation.

    Args:
        reservation_id (int): The id of the reservation.
        service (IReservationService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The started reservation details.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if reservation := await service.get_by_id(reservation_id):
        if str(reservation.user_id) != user_uuid:
             raise HTTPException(status_code=403, detail="Unauthorized")

        try:
            started_reservation = await service.start_reservation(reservation_id)
            return started_reservation.model_dump() if started_reservation else {}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    raise HTTPException(status_code=404, detail="Reservation not found")


@router.put(
        "/end/{reservation_id}",
        response_model=ReservationDTO,
        status_code=200,
)
@inject
async def end_reservation(
    reservation_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for ending reservation.

    Args:
        reservation_id (int): The id of the reservation.
        service (IReservationService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The completed reservation details.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if reservation := await service.get_by_id(reservation_id):
        if str(reservation.user_id) != user_uuid:
             raise HTTPException(status_code=403, detail="Unauthorized")

        try:
            completed_reservation = await service.complete_reservation(reservation_id)
            return completed_reservation.model_dump() if completed_reservation else {}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    raise HTTPException(status_code=404, detail="Reservation not found")
