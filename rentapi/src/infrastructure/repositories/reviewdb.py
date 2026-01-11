"""Module containing review repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from src.core.repositories.ireview import IReviewRepository
from src.core.domain.review import Review, ReviewBroker
from src.db import (
    review_table,
    car_table,
    user_table,
    database)
from src.infrastructure.dto.reviewdto import ReviewDTO


class ReviewRepository(IReviewRepository):
    """A class representing review DB repository."""

    # noinspection PyTestUnpassedFixture
    async def get_all_reviews(self) -> Iterable[Any]:
        """The method getting all reviews from the data storage.

        Returns:
            Iterable[Any]: Review in the data storage
        """

        query = (
            select(review_table, user_table, car_table)
            .select_from(
                review_table
                .join(
                    car_table,
                    review_table.c.car_id == car_table.c.id
                )
                .join(
                    user_table,
                    review_table.c.user_id == user_table.c.id)

            )
            .order_by(review_table.c.id.asc())
        )

        reviews = await database.fetch_all(query)

        return [ReviewDTO.from_record(review) for review in reviews]

    # noinspection PyTestUnpassedFixture
    async def get_by_id(self, review_id: int) -> Any | None:
        """The method getting review provided by id.

        Args:
            review_id (int): The id of the review.

        Returns:
            Any | None: The review details.
        """

        query = (
            select(review_table, user_table, car_table)
            .select_from(
                review_table
                .join(
                    car_table,
                    review_table.c.car_id == car_table.c.id
                )
                .join(
                    user_table,
                    review_table.c.user_id == user_table.c.id
                )
            )
            .where(review_table.c.id == review_id)
            .order_by(review_table.c.id.asc())
        )

        review = await database.fetch_one(query)

        return ReviewDTO.from_record(review) if review else None

    async def get_review_by_car(self, car_id: int) -> Iterable[Any]:
        """The method getting reviews assigned to particular car.

        Args:
            car_id (int): The id of the car.

        Returns:
            Iterable[Any]: Review assigned to a car.
        """

        query = review_table \
            .select() \
            .where(review_table.c.car_id == car_id) \
            .order_by(review_table.c.id.asc())

        reviews = await database.fetch_all(query)

        return [ReviewDTO.from_record(review) for review in reviews]

    async def get_review_by_user(self, user_id: str) -> Iterable[Any]:
        """The method getting reviews assigned to particular user.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Any]: Review assigned to a user.
        """

        query = review_table \
            .select() \
            .where(review_table.c.user_id == user_id) \
            .order_by(review_table.c.id.asc())

        reviews = await database.fetch_all(query)

        return [ReviewDTO.from_record(review) for review in reviews]

    async def add_review(self, data: ReviewBroker) -> Any | None:
        """The method adding new review to the data storage.

        Args:
            data (ReviewBroker): The details of the new review.

        Returns:
            Any | None: The newly added review.
        """

        query = review_table.insert().values(**data.model_dump())
        new_review_id = await database.execute(query)
        new_review = await self._get_by_id(new_review_id)

        return Review(**dict(new_review)) if new_review else None

    async def update_review(
            self,
            review_id: int,
            data: ReviewBroker
    ) -> Any | None:
        """The method updating review data in the data storage.

        Args:
            review_id (int): The id of the car
            data (ReviewBroker): The details of the update review.

        Returns:
            Any | None: The updated review details.
        """

        if self._get_by_id(review_id):
            query = (
                review_table.update()
                .where(review_table.c.id == review_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            review = await self._get_by_id(review_id)

            return Review(**dict(review)) if review else None

        return None

    async def delete_review(self, review_id: int) -> bool:
        """The method removing review from the data storage.

        Args:
             review_id (int): The id of the review.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(review_id):
            query = review_table \
                .delete() \
                .where(review_table.c.id == review_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, review_id: int) -> Record | None:
        """A private method getting review from the DB based on its ID.

        Args:
            review_id (int): The ID of the review.

        Returns:
            Any | None: Review record if exists.
        """

        query = (
            review_table.select()
            .where(review_table.c.id == review_id)
            .order_by(review_table.c.id.asc())
        )

        return await database.fetch_one(query)
