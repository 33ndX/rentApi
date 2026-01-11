"""Module containing review service implementation."""

from typing import Iterable

from src.core.domain.review import Review, ReviewBroker
from src.infrastructure.dto.reviewdto import ReviewDTO
from src.core.repositories.ireservation import IReservationRepository
from src.core.repositories.ireview import IReviewRepository
from src.infrastructure.services.ireview import IReviewService


class ReviewService(IReviewService):
    """A class implementing the review service."""

    _repository: IReviewRepository
    _reservation_repository: IReservationRepository

    def __init__(
            self,
            repository: IReviewRepository,
            reservation_repository: IReservationRepository
    ):
        """The initializer of the `review service`.

        Args:
            repository (IReviewRepository): The reference to the repository.
            reservation_repository (IReservationRepository): The reference to the reservation repository.
        """

        self._repository = repository
        self._reservation_repository = reservation_repository

    async def get_reviews(self) -> Iterable[ReviewDTO]:
        """The method getting all reviews from the repository.

        Returns:
            Iterable[ReviewDTO]: All reviews.
        """

        return await self._repository.get_all_reviews()

    async def get_review_by_id(self, review_id: int) -> ReviewDTO | None:
        """The method getting review by provided id.

        Args:
            review_id (int): The id of the review.

        Returns:
            CarDTO | None: The review details.
        """

        return await self._repository.get_by_id(review_id)

    async def get_review_by_user(self, user_id: str) -> Iterable[ReviewDTO] | None:
        """The method getting reviews by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[ReviewDTO]: The review collection.
        """

        return await self._repository.get_review_by_user(user_id)

    async def get_review_by_car(self, car_id: int) -> Iterable[ReviewDTO]:
        """The method getting reviews assigned to particular car

        Args:
            car_id (int): The id of the car.

        Returns:
            Iterable[ReviewDTO]: The review collection.
        """

        return await self._repository.get_review_by_car(car_id)

    async def add_review(self, data: ReviewBroker) -> Review | None:
        """The method adding new review to the data storage.

        Args:
            data (ReviewBroker): The details of the new review.

        Returns:
            Review | None: Full details of the newly added review.
        """

        has_completed_reservation = await self._reservation_repository.has_completed(
            user_id=data.user_id,
            car_id=data.car_id
        )

        if not has_completed_reservation:
            raise ValueError("No completed reservation for this car")

        return await self._repository.add_review(data=data)

    async def update_review(
        self,
        review_id: int,
        data: ReviewBroker,
    ) -> Review | None:
        """The method updating review data in the data storage.

        Args:
            review_id (int): The id of the review.
            data (ReviewBroker): The details of the updated review.

        Returns:
            Airport | None: The updated review details.
        """

        return await self._repository.update_review(
            review_id=review_id,
            data=data
        )

    async def delete_review(self, review_id: int) -> bool:
        """The method updating removing review from the data storage.

        Args:
            review_id (int): The id of the review.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_review(review_id)
