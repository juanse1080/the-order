from fastapi import APIRouter, Depends
from app.di import get_product_service, get_restaurant_service
from app.schemas.common_schema import PaginationInput
from app.schemas.product_schema import ProductListResponse, ProductResponse
from app.schemas.restaurant_schema import (
    CreateRestaurant,
    RestaurantListResponse,
    RestaurantResponse,
    UpdateRestaurant,
)
from app.services.product_service import ProductService
from app.services.restaurant_service import RestaurantService

router = APIRouter()


@router.get("/restaurant", response_model=RestaurantListResponse)
async def list_restaurants(
    pagination: PaginationInput = Depends(),
    restaurant_service: RestaurantService = Depends(get_restaurant_service),
):
    return await restaurant_service.list(page=pagination.page, limit=pagination.limit)


@router.post("/restaurant", response_model=RestaurantResponse, status_code=201)
async def create_restaurant(
    restaurant_input: CreateRestaurant,
    restaurant_service: RestaurantService = Depends(get_restaurant_service),
):
    return await restaurant_service.create(restaurant_input)


@router.get("/restaurant/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(
    restaurant_id: int,
    restaurant_service: RestaurantService = Depends(get_restaurant_service),
):
    return await restaurant_service.get_by_id(restaurant_id)


@router.patch("/restaurant/{restaurant_id}", response_model=RestaurantResponse)
async def update_restaurant(
    restaurant_id: int,
    restaurant_input: UpdateRestaurant,
    restaurant_service: RestaurantService = Depends(get_restaurant_service),
):
    return await restaurant_service.update(restaurant_id, restaurant_input)


@router.delete("/restaurant/{restaurant_id}", response_model=RestaurantResponse)
async def delete_restaurant(
    restaurant_id: int,
    restaurant_service: RestaurantService = Depends(get_restaurant_service),
):
    return await restaurant_service.delete(restaurant_id)
