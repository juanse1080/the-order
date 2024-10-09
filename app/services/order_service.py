from ..repositories.line_item_repository import LineItemRepository
from ..repositories.order_repository import OrderRepository
from ..repositories.restaurant_repository import RestaurantRepository
from ..models.order_model import LineItemModel, OrderModel
from ..schemas.order_schema import (
    CreateLineItem,
    CreateOrder,
    CreateOrderInput,
    LineItemResponse,
    OrderDetailResponse,
    OrderListResponse,
    OrderResponse,
    StateCode,
)
from ..schemas.restaurant_schema import RestaurantResponse


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        line_item_repository: LineItemRepository,
        restaurant_repository: RestaurantRepository,
    ):
        self.order_repository = order_repository
        self.line_item_repository = line_item_repository
        self.restaurant_repository = restaurant_repository

    def __transform_to_detail(self, order: OrderModel, line_items: list[LineItemModel]):
        return {
            "id": order.id,
            "buyer_name": order.buyer_name,
            "restaurant_id": order.restaurant_id,
            "state_code": order.state_code,
            "package_code": order.package_code,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "line_items": [
                {
                    "id": item.id,
                    "order_id": order.id,
                    "product_id": item.product_id,
                    "qyt_ordened": item.qyt_ordened,
                    "comments": item.comments,
                    "created_at": item.created_at,
                    "updated_at": item.updated_at,
                }
                for item in line_items
            ],
        }

    async def __get_or_fail(self, id: int) -> OrderResponse:
        order = await self.order_repository.get_by_id(id=id)
        if not order:
            raise Exception("Order not found")
        return order

    async def __get_or_fail_restaurant(self, id: int) -> RestaurantResponse:
        restaurant = await self.restaurant_repository.get_by_id(id=id)
        if not restaurant:
            raise Exception("Restaurant not found")
        return restaurant

    async def list(
        self, restaurant_id: int, page: int, limit: int
    ) -> OrderListResponse:
        await self.__get_or_fail_restaurant(id=restaurant_id)

        orders = await self.order_repository.list(
            restaurant_id=restaurant_id, page=page, limit=limit
        )
        count = await self.order_repository.count(restaurant_id=restaurant_id)

        return {
            "data": orders,
            "meta_data": {
                "page": page,
                "limit": limit,
                "total_count": count,
            },
        }

    async def create(
        self, restaurant_id: int, input: CreateOrderInput
    ) -> OrderDetailResponse:
        await self.__get_or_fail_restaurant(id=restaurant_id)

        order = await self.order_repository.create(
            restaurant_id=restaurant_id,
            input=CreateOrder(
                buyer_name=input.buyer_name,
                state_code=StateCode.PENDING.value,
                package_code=input.package_code,
            ),
        )

        await self.line_item_repository.create_many(
            order_id=order.id,
            input=[
                CreateLineItem(
                    product_id=item.product_id,
                    qyt_ordened=item.qyt_ordened,
                    comments=item.comments,
                )
                for item in input.line_items
            ],
        )

        line_items = await self.line_item_repository.list_by_order(order_id=order.id)

        return self.__transform_to_detail(order=order, line_items=line_items)

    async def get_by_id(self, id: int) -> OrderDetailResponse:
        order = await self.__get_or_fail(id=id)
        line_items = await self.line_item_repository.list_by_order(order_id=order.id)
        return self.__transform_to_detail(order=order, line_items=line_items)

    async def delete(self, id: int) -> OrderResponse:
        await self.__get_or_fail(id)
        return await self.order_repository.delete(id=id)
