from fastapi import HTTPException
from ..repositories.restaurant_repository import RestaurantRepository
from ..schemas.restaurant_schema import (
    CreateRestaurant,
    RestaurantListResponse,
    RestaurantResponse,
    UpdateRestaurant,
)


class RestaurantService:
    def __init__(self, restaurant_repository: RestaurantRepository):
        self.restaurant_repository = restaurant_repository

    async def __get_or_fail(self, id: int) -> RestaurantResponse:
        restaurant = await self.restaurant_repository.get_by_id(id=id)
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        return restaurant

    async def list(self, page: int, limit: int) -> RestaurantListResponse:
        restaurants = await self.restaurant_repository.list(page=page, limit=limit)

        count = await self.restaurant_repository.count()

        return {
            "data": restaurants,
            "meta_data": {
                "page": page,
                "limit": limit,
                "total_count": count,
            },
        }

    async def create(self, input: CreateRestaurant) -> RestaurantResponse:
        return await self.restaurant_repository.create(input=input)

    async def get_by_id(self, id: int) -> RestaurantResponse:
        return await self.__get_or_fail(id=id)

    async def update(self, id: int, input: UpdateRestaurant) -> RestaurantResponse:
        await self.__get_or_fail(id)
        return await self.restaurant_repository.update(id=id, input=input)

    async def delete(self, id: int) -> RestaurantResponse:
        await self.__get_or_fail(id)
        return await self.restaurant_repository.delete(id=id)
