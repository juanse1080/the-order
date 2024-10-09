from sqlalchemy import delete, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional

from app.models.product_model import ProductModel
from app.schemas.product_schema import CreateProduct, UpdateProduct


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(
        self,
        restaurant_id: int,
        page: int,
        limit: int,
    ) -> list[ProductModel]:
        result = await self.db.execute(
            select(ProductModel)
            .where(ProductModel.restaurant_id == restaurant_id)
            .offset(limit * page)
            .limit(limit)
        )
        products = result.scalars().all()
        return products

    async def count(
        self,
        restaurant_id: int,
    ) -> int:
        result = await self.db.execute(
            select(func.count(ProductModel.id)).where(
                ProductModel.restaurant_id == restaurant_id
            )
        )
        count = result.scalar_one_or_none()
        return count or 0

    async def create(self, restaurant_id: int, input: CreateProduct) -> ProductModel:
        product = ProductModel(
            restaurant_id=restaurant_id,
            **input.dict(exclude_unset=True),
        )
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def get_by_id(self, id: int) -> Optional[ProductModel]:
        result = await self.db.execute(
            select(ProductModel).where(ProductModel.id == id)
        )
        restaurant = result.scalar_one_or_none()
        return restaurant

    async def update(self, id: int, input: UpdateProduct) -> Optional[ProductModel]:
        await self.db.execute(
            update(ProductModel)
            .where(ProductModel.id == id)
            .values(**input.dict(exclude_unset=True))
        )
        restaurant = await self.get_by_id(id)
        return restaurant

    async def delete(self, id: int) -> Optional[ProductModel]:
        restaurant = await self.get_by_id(id)
        await self.db.execute(delete(ProductModel).where(ProductModel.id == id))
        return restaurant
