from sqlalchemy import delete, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.restaurant_model import RestaurantModel
from typing import Optional

from ..schemas.restaurant_schema import CreateRestaurant, UpdateRestaurant


class RestaurantRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(
        self,
        page: int,
        limit: int,
    ) -> list[RestaurantModel]:
        result = await self.db.execute(
            select(RestaurantModel).offset(limit * page).limit(limit)
        )
        restaurants = result.scalars().all()
        return restaurants

    async def count(
        self,
    ) -> int:
        result = await self.db.execute(select(func.count(RestaurantModel.id)))
        count = result.scalar_one_or_none()
        return count or 0

    async def create(self, input: CreateRestaurant) -> RestaurantModel:
        restaurant = RestaurantModel(**input.dict(exclude_unset=True))
        self.db.add(restaurant)
        await self.db.commit()
        await self.db.refresh(restaurant)
        print({"restaurant": restaurant})
        return restaurant

    async def get_by_id(self, id: int) -> Optional[RestaurantModel]:
        result = await self.db.execute(
            select(RestaurantModel).where(RestaurantModel.id == id)
        )
        restaurant = result.scalar_one_or_none()
        return restaurant

    async def update(
        self, id: int, input: UpdateRestaurant
    ) -> Optional[RestaurantModel]:

        await self.db.execute(
            update(RestaurantModel)
            .where(RestaurantModel.id == id)
            .values(**input.dict(exclude_unset=True))
        )

        restaurant = await self.get_by_id(id)
        return restaurant

    async def delete(self, id: int) -> Optional[RestaurantModel]:
        restaurant = await self.get_by_id(id)
        await self.db.execute(delete(RestaurantModel).where(RestaurantModel.id == id))
        return restaurant
