from typing import List
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String
from ..models.common_model import TimestampMixin, Base
from sqlalchemy.orm import Mapped


class ProductModel(TimestampMixin, Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
    description = Column(String, nullable=True)
    price = Column(Integer)

    restaurant_id = Column(Integer, ForeignKey("restaurant.id", ondelete="CASCADE"))

    line_items: Mapped[List["LineItemModel"]] = relationship(
        "LineItemModel", back_populates="product", lazy="selectin"
    )
