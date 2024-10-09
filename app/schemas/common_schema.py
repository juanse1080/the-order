from typing import Optional
from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field


class TimestampResponse:
    created_at: datetime
    updated_at: Optional[datetime]


class MetadataResponse(BaseModel):
    page: int
    limit: int
    total_count: int


class PaginationInput(BaseModel):
    page: int = Field(Query(default=0, ge=0))
    limit: int = Field(Query(default=10, ge=1))
