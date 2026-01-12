"""A module containing payment endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.infrastructure.utils import consts
from src.container import Container
from src.infrastructure.dto.paymentdto import PaymentDTO
from src.infrastructure.services.ipayment import IPaymentService

bearer_scheme = HTTPBearer()

router = APIRouter()


@router.post("/pay/{reservation_id}", response_model=PaymentDTO, status_code=201)
@inject
async def pay_for_reservation(
    reservation_id: int,
    service: IPaymentService = Depends(Provide[Container.payment_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for processing payment for a reservation.

    Args:
        reservation_id (int): The id of the reservation.
        service (IPaymentService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The processed payment details.
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
        payment = await service.process_payment(
            reservation_id=reservation_id,
            user_id=user_uuid,
        )

        return payment.model_dump() if payment else {}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/my",
    response_model=Iterable[PaymentDTO],
    status_code=200
)
@inject
async def get_my_payments(
    service: IPaymentService = Depends(Provide[Container.payment_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Iterable:
    """An endpoint for getting the current user's payments.

    Args:
        service (IPaymentService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        Iterable: The payment details collection.
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

    payments = await service.get_by_user(user_uuid)

    return payments
