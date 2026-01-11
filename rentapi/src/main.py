"""Main module of the app"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from src.api.routers.car import router as car_router
from src.api.routers.user import router as user_router
from src.api.routers.reservation import router as reservation_router
from src.api.routers.review import router as review_router
from src.api.routers.payment import router as payment_router
from src.container import Container
from src.db import database, init_db

container = Container()
container.wire(modules=[
    "src.api.routers.car",
    "src.api.routers.reservation",
    "src.api.routers.review",
    "src.api.routers.payment",
    "src.api.routers.user",
    ])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(car_router, prefix="/car")
app.include_router(reservation_router, prefix="/reservations")
app.include_router(review_router, prefix="/reviews")
app.include_router(payment_router, prefix="/payment")
app.include_router(user_router, prefix="")


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    """A function handling http exceptions for logging purposes.

    Args:
        request (Request): The incoming HTTP request.
        exception (HTTPException): A related exception.

    Returns:
        Response: The HTTP response.
    """
    return await http_exception_handler(request, exception)
