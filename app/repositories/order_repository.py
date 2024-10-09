from typing import Optional
from sqlalchemy import delete, func, select, update
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.order_model import LineItemModel, OrderModel
from ..schemas.order_schema import (
    CreateOrder,
    CreateOrderInput,
    StateCode,
    UpdateOrderInput,
)


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
            .distinct(OrderModel.id)
            .join(OrderModel.line_items)
            .join(LineItemModel.product)
            .options(
                selectinload(OrderModel.line_items).selectinload(LineItemModel.product)
            )
            .add_columns(LineItemModel.product)
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

    async def create(self, restaurant_id: int, input: CreateOrderInput) -> OrderModel:
        order = OrderModel(
            restaurant_id=restaurant_id,
            buyer_name=input.buyer_name,
            state_code=StateCode.PENDING.value,
            package_code=input.package_code,
        )

        order.line_items = [
            LineItemModel(
                product_id=item.product_id,
                qyt_ordened=item.qyt_ordened,
                comments=item.comments,
            )
            for item in input.line_items
        ]

        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order

    async def get_by_id(self, id: int) -> Optional[OrderModel]:
        result = await self.db.execute(
            select(OrderModel)
            .join(OrderModel.line_items)
            .join(LineItemModel.product)
            .options(
                selectinload(OrderModel.line_items).selectinload(LineItemModel.product)
            )
            .add_columns(LineItemModel.product)
            .distinct(OrderModel.id)
            .where(OrderModel.id == id)
        )
        order = result.scalar_one_or_none()
        return order

    async def update(self, id: int, input: UpdateOrderInput) -> Optional[OrderModel]:
        await self.db.execute(
            update(OrderModel)
            .where(OrderModel.id == id)
            .values(**input.dict(exclude_unset=True))
        )
        await self.db.commit()

        order = await self.get_by_id(id)
        return order

    async def delete(self, id: int) -> Optional[OrderModel]:
        order = await self.get_by_id(id)
        await self.db.execute(delete(OrderModel).where(OrderModel.id == id))
        return order
