from fastapi import APIRouter, Depends

from ..di import get_order_service
from ..schemas.common_schema import PaginationInput
from ..schemas.order_schema import (
    CreateOrderInput,
    OrderDetailResponse,
    OrderListResponse,
    OrderResponse,
)
from ..services.order_service import OrderService


router = APIRouter()


@router.get("/restaurant/{restaurant_id}/order", response_model=OrderListResponse)
async def list_orders(
    restaurant_id: int,
    pagination: PaginationInput = Depends(),
    order_service: OrderService = Depends(get_order_service),
):
    return await order_service.list(
        restaurant_id=restaurant_id, page=pagination.page, limit=pagination.limit
    )


@router.post(
    "/restaurant/{restaurant_id}/order",
    response_model=OrderDetailResponse,
    status_code=201,
)
async def create_order(
    restaurant_id: int,
    order_input: CreateOrderInput,
    order_service: OrderService = Depends(get_order_service),
):
    return await order_service.create(restaurant_id=restaurant_id, input=order_input)


@router.get("/order/{order_id}", response_model=OrderDetailResponse)
async def get_order(
    order_id: int,
    order_service: OrderService = Depends(get_order_service),
):
    return await order_service.get_by_id(id=order_id)


@router.delete("/order/{order_id}", response_model=OrderResponse)
async def delete_order(
    order_id: int,
    order_service: OrderService = Depends(get_order_service),
):
    return await order_service.delete(id=order_id)
