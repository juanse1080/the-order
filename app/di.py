from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .repositories.line_item_repository import LineItemRepository
from .repositories.order_repository import OrderRepository
from .repositories.product_repository import ProductRepository
from .repositories.restaurant_repository import RestaurantRepository
from .db.connection import get_db
from .services.order_service import OrderService
from .services.product_service import ProductService
from .services.restaurant_service import RestaurantService


async def get_restaurant_repository(
    db: AsyncSession = Depends(get_db),
) -> RestaurantRepository:
    return RestaurantRepository(db)


async def get_product_repository(
    db: AsyncSession = Depends(get_db),
) -> ProductRepository:
    return ProductRepository(db)


async def get_order_repository(
    db: AsyncSession = Depends(get_db),
) -> OrderRepository:
    return OrderRepository(db)


async def get_line_item_repository(
    db: AsyncSession = Depends(get_db),
) -> LineItemRepository:
    return LineItemRepository(db)


async def get_product_service(
    product_repository: ProductRepository = Depends(get_product_repository),
    restaurant_repository: RestaurantRepository = Depends(get_restaurant_repository),
) -> ProductService:
    return ProductService(product_repository, restaurant_repository)


async def get_restaurant_service(
    user_repository: RestaurantRepository = Depends(get_restaurant_repository),
) -> RestaurantService:
    return RestaurantService(user_repository)


async def get_order_service(
    order_repository: OrderRepository = Depends(get_order_repository),
    restaurant_repository: RestaurantRepository = Depends(get_restaurant_repository),
) -> OrderService:
    return OrderService(order_repository, restaurant_repository)
