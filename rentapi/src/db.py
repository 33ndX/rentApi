"""A module for providing database access."""

import asyncio

import databases
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.mutable import MutableList
from asyncpg.exceptions import (    # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)

from rentapi.src.config import config

metadata = sqlalchemy.MetaData()

car_table = sqlalchemy.Table(
    "cars",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("brand", sqlalchemy.String),
    sqlalchemy.Column("model",  sqlalchemy.String),
    sqlalchemy.Column("year", sqlalchemy.String),
    sqlalchemy.Column("registration_number", sqlalchemy.String),
    sqlalchemy.Column("mileage", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("fuel_type", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("gearbox", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("seats", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=True),
)
