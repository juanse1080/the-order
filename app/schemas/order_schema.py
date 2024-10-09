from enum import Enum
from typing import Optional
from pydantic import BaseModel

from app.schemas.product_schema import ProductResponse
from ..schemas.common_schema import MetadataResponse, TimestampResponse


class StateCode(Enum):
    PENDING = "PENDING"
    PREPARED = "PREPARED"
    DELIVERED = "DELIVERED"
    IN_PREPARATION = "IN_PREPARATION"


class PackageCode(Enum):
    TO_GO = "TO_GO"
    EAT_HERE = "EAT_HERE"


class LineItemResponse(TimestampResponse, BaseModel):
    id: int
    qyt_ordened: int
    comments: str
    order_id: int
    product_id: int
    product: ProductResponse

    class Config:
        orm_mode = True


class OrderDetailResponse(TimestampResponse, BaseModel):
    id: int
    buyer_name: str
    restaurant_id: int
    state_code: str
    package_code: str


class OrderResponse(TimestampResponse, BaseModel):
    id: int
    buyer_name: str
    restaurant_id: int
    state_code: str
    package_code: str
    line_items: list[LineItemResponse]

    class Config:
        orm_mode = True


class OrderListResponse(BaseModel):
    data: list[OrderResponse]
    meta_data: MetadataResponse


class CreateLineItem(BaseModel):
    product_id: int
    qyt_ordened: int
    comments: Optional[str] = None


class CreateOrder(BaseModel):
    buyer_name: str
    state_code: str
    package_code: str


class CreateOrderInput(BaseModel):
    buyer_name: str
    package_code: str
    line_items: list[CreateLineItem]


class UpdateOrderInput(BaseModel):
    state_code: Optional[str] = None
    package_code: Optional[str] = None
