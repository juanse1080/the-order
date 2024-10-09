from typing import Optional
from pydantic import BaseModel
from ..schemas.common_schema import TimestampResponse, MetadataResponse


class ProductResponse(TimestampResponse, BaseModel):
    id: int
    name: str
    image: str
    description: str
    price: int
    restaurant_id: int

    class Config:
        orm_mode = True


class ProductListResponse(BaseModel):
    data: list[ProductResponse]
    meta_data: MetadataResponse


class CreateProduct(BaseModel):
    name: str
    image: str
    description: str
    price: int


class UpdateProduct(BaseModel):
    name: Optional[str] | None = None
    image: Optional[str] | None = None
    description: Optional[str] | None = None
    price: Optional[int] | None = None
