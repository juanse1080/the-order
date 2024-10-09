from typing import Optional
from pydantic import BaseModel
from ..schemas.common_schema import MetadataResponse, TimestampResponse


class RestaurantResponse(TimestampResponse, BaseModel):
    id: int
    name: str
    logo: str

    class Config:
        orm_mode = True


class RestaurantListResponse(BaseModel):
    data: list[RestaurantResponse]
    meta_data: MetadataResponse


class CreateRestaurant(BaseModel):
    name: str
    logo: str


class UpdateRestaurant(BaseModel):
    name: Optional[str] = None
    logo: Optional[str] = None
