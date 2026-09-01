"""FastAPI implementation of the Order Tracking API contract."""
from datetime import datetime
import re

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

app = FastAPI(title="Order Tracking API", version="1.0.0")

ORDER_ID_PATTERN = re.compile(r"^ORD-[0-9]{4}$")


class Order(BaseModel):
    model_config = ConfigDict(extra="forbid")

    order_id: str
    customer: str
    status: str
    destination: str
    expected_delivery: datetime


class ErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str


class BackendUnavailableError(Exception):
    pass


ORDERS = {
    "ORD-1001": {
        "customer": "ABC Retail",
        "status": "SHIPPED",
        "destination": "Pune",
        "expected_delivery": "2026-08-25T18:00:00Z",
    },
    "ORD-1002": {
        "customer": "XYZ Industries",
        "status": "PROCESSING",
        "destination": "Mumbai",
        "expected_delivery": "2026-08-28T18:00:00Z",
    },
}


@app.exception_handler(BackendUnavailableError)
async def backend_unavailable_handler(
    request: Request, exception: BackendUnavailableError
) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"message": "Order service temporarily unavailable."},
    )


@app.get(
    "/api/orders/{order_id}",
    response_model=Order,
    operation_id="getOrder",
    responses={
        400: {"model": ErrorResponse, "description": "The order ID is invalid."},
        404: {"model": ErrorResponse, "description": "The order was not found."},
        503: {
            "model": ErrorResponse,
            "description": "The order backend is unavailable.",
        },
    },
)
async def get_order(order_id: str) -> Order:
    if not ORDER_ID_PATTERN.fullmatch(order_id):
        return JSONResponse(
            status_code=400, content={"message": "Invalid order ID."}
        )

    try:
        order = ORDERS.get(order_id)
        if order is None:
            return JSONResponse(
                status_code=404, content={"message": "Order not found."}
            )
        return Order(order_id=order_id, **order)
    except BackendUnavailableError:
        raise
    except Exception as exception:
        raise BackendUnavailableError from exception
