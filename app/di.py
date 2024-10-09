from fastapi import Depends
from app.adapters.repositories.line_item_repository import LineItemRepository
from app.adapters.repositories.order_repository import OrderRepository
from app.adapters.repositories.product_repository import ProductRepository
from app.adapters.repositories.restaurant_repository import RestaurantRepository
from app.db.connection import get_db
from app.services.order_service import OrderService
from app.services.product_service import ProductService
from app.services.restaurant_service import RestaurantService
from sqlalchemy.ext.asyncio import AsyncSession


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
    line_item_repository: LineItemRepository = Depends(get_line_item_repository),
    restaurant_repository: RestaurantRepository = Depends(get_restaurant_repository),
) -> OrderService:
    return OrderService(order_repository, line_item_repository, restaurant_repository)
