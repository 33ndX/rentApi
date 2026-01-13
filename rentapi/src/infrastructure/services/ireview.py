"""Module containing review service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4


from src.core.domain.review import Review, ReviewBroker
from src.infrastructure.dto.reviewdto import ReviewDTO


class IReviewService(ABC):
    """A class representing a review repository."""

    @abstractmethod
    async def get_reviews(self) -> Iterable[ReviewDTO]:
        """The method getting all reviews from the repository.

        Returns:
            Iterable[ReviewDTO]: All reviews.
        """

    @abstractmethod
    async def get_review_by_id(self, review_id: int) -> ReviewDTO | None:
        """The method getting review by provided id.

        Args:
            review_id (int): The id of the review.

        Returns:
            CarDTO | None: The review details.
        """

    @abstractmethod
    async def get_review_by_user(self, user_id: str) -> Iterable[ReviewDTO] | None:
        """The method getting reviews by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[ReviewDTO]: The review collection.
        """

    @abstractmethod
    async def get_review_by_car(self, car_id: int) -> Iterable[ReviewDTO]:
        """The method getting reviews assigned to particular car

        Args:
            car_id (int): The id of the car.

        Returns:
            Iterable[ReviewDTO]: The review collection.
        """

    @abstractmethod
    async def add_review(self, data: ReviewBroker) -> Review | None:
        """The method adding new review to the data storage.

        Args:
            data (ReviewBroker): The details of the new review.

        Returns:
            Review | None: Full details of the newly added review.
        """

    @abstractmethod
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
            Review | None: The updated review details.
        """

    @abstractmethod
    async def delete_review(self, review_id: int) -> bool:
        """The method updating removing review from the data storage.

        Args:
            review_id (int): The id of the review.

        Returns:
            bool: Success of the operation.
        """