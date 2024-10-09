from fastapi import HTTPException
from ..repositories.product_repository import ProductRepository
from ..repositories.restaurant_repository import RestaurantRepository
from ..schemas.product_schema import (
    CreateProduct,
    ProductListResponse,
    ProductResponse,
    UpdateProduct,
)
from ..schemas.restaurant_schema import RestaurantResponse


class ProductService:
    def __init__(
        self,
        product_repository: ProductRepository,
        restaurant_repository: RestaurantRepository,
    ):
        self.product_repository = product_repository
        self.restaurant_repository = restaurant_repository

    async def __get_or_fail(self, id: int) -> ProductResponse:
        product = await self.product_repository.get_by_id(id=id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    async def __get_or_fail_restaurant(self, id: int) -> RestaurantResponse:
        restaurant = await self.restaurant_repository.get_by_id(id=id)
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        return restaurant

    async def list(
        self, restaurant_id: int, page: int, limit: int
    ) -> ProductListResponse:
        await self.__get_or_fail_restaurant(id=restaurant_id)

        products = await self.product_repository.list(
            restaurant_id=restaurant_id, page=page, limit=limit
        )
        count = await self.product_repository.count(restaurant_id=restaurant_id)

        return {
            "data": products,
            "meta_data": {
                "page": page,
                "limit": limit,
                "total_count": count,
            },
        }

    async def create(self, restaurant_id: int, input: CreateProduct) -> ProductResponse:
        await self.__get_or_fail_restaurant(id=restaurant_id)

        return await self.product_repository.create(
            restaurant_id=restaurant_id, input=input
        )

    async def get_by_id(self, id: int) -> ProductResponse:
        return await self.__get_or_fail(id=id)

    async def update(self, id: int, input: UpdateProduct) -> ProductResponse:
        await self.__get_or_fail(id)
        return await self.product_repository.update(id=id, input=input)

    async def delete(self, id: int) -> ProductResponse:
        await self.__get_or_fail(id)
        return await self.product_repository.delete(id=id)
