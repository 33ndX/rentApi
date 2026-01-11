"""Modul containing review-related domain models."""


from abc import ABC, abstractmethod
from typing import Any, Iterable

from src.core.domain.review import ReviewBroker


class IReviewRepository(ABC):
    """An abstract class representing protocol of review repository."""

    @abstractmethod
    async def get_all_reviews(self) -> Iterable[Any]:
        """The abstract getting all reviews from the data storage.

        Returns:
            Iterable[Any]: Review in the data storage
        """

    @abstractmethod
    async def get_by_id(self, review_id: int) -> Any | None:
        """The abstract getting review provided by id.

        Args:
            review_id (int): The id of the review.

        Returns:
            Any | None: The review details.
        """

    @abstractmethod
    async def get_review_by_car(self, car_id: int) -> Iterable[Any]:
        """The abstract getting reviews assigned to particular car.

        Args:
            car_id (int): The id of the car.

        Returns:
            Iterable[Any]: Review assigned to a car.
        """

    @abstractmethod
    async def get_review_by_user(self, user_id: str) -> Iterable[Any]:
        """The abstract getting reviews assigned to particular user.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Any]: Review assigned to a user.
        """

    @abstractmethod
    async def add_review(self, data: ReviewBroker) -> Any | None:
        """The abstract adding new review to the data storage.

        Args:
            data (ReviewBroker): The details of the new review.

        Returns:
            Any | None: The newly added review.
        """

    @abstractmethod
    async def update_review(
            self,
            review_id: int,
            data: ReviewBroker
    ) -> Any | None:
        """The abstract updating review data in the data storage.

        Args:
            review_id (int): The id of the car
            data (ReviewBroker): The details of the update review.

        Returns:
            Any | None: The updated review details.
        """

    @abstractmethod
    async def delete_review(self, review_id: int) -> bool:
        """The abstract removing review from the data storage.

        Args:
             review_id (int): The id of the review.

        Returns:
            bool: Success of the operation.
        """
