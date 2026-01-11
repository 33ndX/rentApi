"""A module containing review endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.infrastructure.utils import consts
from src.container import Container
from src.core.domain.review import Review, ReviewIn, ReviewBroker
from src.infrastructure.dto.reviewdto import ReviewDTO
from src.infrastructure.services.ireview import IReviewService

bearer_scheme = HTTPBearer()

router = APIRouter()


@router.post("/create", response_model=Review, status_code=201)
@inject
async def create_review(
        review: ReviewIn,
        service: IReviewService = Depends(Provide[Container.review_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for adding new review.

    Args:
        review (ReviewIn): The review data.
        service (IReviewService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The new review attributes.
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
        extended_review_data = ReviewBroker(
            user_id=user_uuid,
            **review.model_dump(),
        )
        new_review = await service.add_review(extended_review_data)

        return new_review.model_dump() if new_review else {}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all", response_model=Iterable[ReviewDTO], status_code=200)
@inject
async def get_all_reviews(
    service: IReviewService = Depends(Provide[Container.review_service]),
) -> Iterable:
    """An endpoint for getting all reviews.

    Args:
        service (IReviewService, optional): The injected service dependency.

    Returns:
        Iterable: The review attributes collection.
    """

    reviews = await service.get_reviews()

    return reviews


@router.get(
        "/{review_id}",
        response_model=ReviewDTO,
        status_code=200,
)
@inject
async def get_review_by_id(
    review_id: int,
    service: IReviewService = Depends(Provide[Container.review_service]),
) -> dict | None:
    """An endpoint for getting review by id.

    Args:
        review_id (int): The id of the review.
        service (IReviewService, optional): The injected service dependency.

    Returns:
        dict | None: The review details.
    """

    if review := await service.get_review_by_id(review_id):
        return review.model_dump()

    raise HTTPException(status_code=404, detail="Review not found")


@router.get(
        "/car/{car_id}",
        response_model=Iterable[ReviewDTO],
        status_code=200,
)
@inject
async def get_reviews_by_car(
    car_id: int,
    service: IReviewService = Depends(Provide[Container.review_service]),
) -> Iterable:
    """An endpoint for getting reviews by car.

    Args:
        car_id (int): The id of the car.
        service (IReviewService, optional): The injected service dependency.

    Returns:
        Iterable: The review details collection.
    """

    reviews = await service.get_review_by_car(car_id)

    return reviews


@router.put("/{review_id}", response_model=Review, status_code=201)
@inject
async def update_review(
    review_id: int,
    updated_review: ReviewIn,
    service: IReviewService = Depends(Provide[Container.review_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating review data.

    Args:
        review_id (int): The id of the review.
        updated_review (ReviewIn): The updated review details.
        service (IReviewService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if review does not exist.

    Returns:
        dict: The updated review details.
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

    if review_data := await service.get_review_by_id(review_id=review_id):
        if str(review_data.user_id) != user_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")

        extended_updated_review = ReviewBroker(
            user_id=user_uuid,
            **updated_review.model_dump(),
        )
        updated_review_data = await service.update_review(
            review_id=review_id,
            data=extended_updated_review,
        )
        return updated_review_data.model_dump() if updated_review_data \
            else {}

    raise HTTPException(status_code=404, detail="Review not found")


@router.delete("/{review_id}", status_code=204)
@inject
async def delete_review(
    review_id: int,
    service: IReviewService = Depends(Provide[Container.review_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting reviews.

    Args:
        review_id (int): The id of the review.
        service (IReviewService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if review does not exist.
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

    if review_data := await service.get_review_by_id(review_id=review_id):
        if str(review_data.user_id) != user_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")

        await service.delete_review(review_id=review_id)
        return

    raise HTTPException(status_code=404, detail="Review not found")
