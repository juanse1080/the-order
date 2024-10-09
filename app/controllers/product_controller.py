from fastapi import APIRouter, Depends
from ..di import get_product_service
from ..schemas.common_schema import PaginationInput
from ..schemas.product_schema import (
    CreateProduct,
    ProductListResponse,
    ProductResponse,
    UpdateProduct,
)
from ..services.product_service import ProductService

router = APIRouter()


@router.get("/restaurant/{restaurant_id}/product", response_model=ProductListResponse)
async def list_products(
    restaurant_id: int,
    pagination: PaginationInput = Depends(),
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.list(
        restaurant_id=restaurant_id, page=pagination.page, limit=pagination.limit
    )


@router.post(
    "/restaurant/{restaurant_id}/product",
    response_model=ProductResponse,
    status_code=201,
)
async def create_product(
    restaurant_id: int,
    product_input: CreateProduct,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.create(
        restaurant_id=restaurant_id, input=product_input
    )


@router.get("/product/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.get_by_id(id=product_id)


@router.patch("/product/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_input: UpdateProduct,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.update(id=product_id, input=product_input)


@router.delete("/product/{product_id}", response_model=ProductResponse)
async def delete_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.delete(id=product_id)
