from typing import Optional
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order_model import OrderModel
from app.schemas.order_schema import CreateOrder


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(
        self,
        restaurant_id: int,
        page: int,
        limit: int,
    ) -> list[OrderModel]:
        result = await self.db.execute(
            select(OrderModel)
            .where(OrderModel.restaurant_id == restaurant_id)
            .offset(limit * page)
            .limit(limit)
        )
        orders = result.scalars().all()
        return orders

    async def count(
        self,
        restaurant_id: int,
    ) -> int:
        result = await self.db.execute(
            select(func.count(OrderModel.id)).where(
                OrderModel.restaurant_id == restaurant_id
            )
        )
        count = result.scalar_one_or_none()
        return count or 0

    async def create(self, restaurant_id: int, input: CreateOrder) -> OrderModel:
        order = OrderModel(
            restaurant_id=restaurant_id,
            **input.dict(exclude_unset=True),
        )

        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def get_by_id(self, id: int) -> Optional[OrderModel]:
        result = await self.db.execute(select(OrderModel).where(OrderModel.id == id))
        order = result.scalar_one_or_none()
        return order

    async def delete(self, id: int) -> Optional[OrderModel]:
        order = await self.get_by_id(id)
        await self.db.execute(delete(OrderModel).where(OrderModel.id == id))
        return order
