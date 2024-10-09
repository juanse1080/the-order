from typing import Optional
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.order_model import LineItemModel
from ..schemas.order_schema import CreateLineItem


class LineItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_order(
        self,
        order_id: int,
    ) -> list[LineItemModel]:
        result = await self.db.execute(
            select(LineItemModel).where(LineItemModel.order_id == order_id)
        )
        orders = result.scalars().all()
        return orders

    async def create(self, order_id: int, input: CreateLineItem) -> LineItemModel:
        item = LineItemModel(
            order_id=order_id,
            **input.dict(exclude_unset=True),
        )

        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def create_many(self, order_id: int, input: list[CreateLineItem]):
        items = [
            {
                "order_id": order_id,
                "comments": item.comments,
                "product_id": item.product_id,
                "qyt_ordened": item.qyt_ordened,
            }
            for item in input
        ]

        await self.db.execute(insert(LineItemModel), items)
        await self.db.commit()

    async def get_by_id(self, id: int) -> Optional[LineItemModel]:
        result = await self.db.execute(
            select(LineItemModel).where(LineItemModel.id == id)
        )
        order = result.scalar_one_or_none()
        return order
