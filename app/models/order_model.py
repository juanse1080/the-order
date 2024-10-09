from typing import List
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from ..models.common_model import TimestampMixin, Base


class StateModel(Base):
    __tablename__ = "state"

    code = Column(String, primary_key=True, unique=True)
    name = Column(String)
    description = Column(String)


class PackageModel(Base):
    __tablename__ = "package"

    code = Column(String, primary_key=True, unique=True)
    name = Column(String)
    description = Column(String)


class OrderModel(TimestampMixin, Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    buyer_name = Column(String)

    state_code = Column(String, ForeignKey("state.code"))
    package_code = Column(String, ForeignKey("package.code"))
    restaurant_id = Column(Integer, ForeignKey("restaurant.id", ondelete="CASCADE"))

    line_items: Mapped[List["LineItemModel"]] = relationship(
        "LineItemModel", back_populates="order", lazy="selectin"
    )


class LineItemModel(TimestampMixin, Base):
    __tablename__ = "line_item"

    id = Column(Integer, primary_key=True)
    qyt_ordened = Column(Integer)
    comments = Column(String, nullable=True)

    order_id = Column(Integer, ForeignKey("order.id", ondelete="CASCADE"))
    order: Mapped["OrderModel"] = relationship(
        "OrderModel",
        back_populates="line_items",
    )

    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"))
    product: Mapped["ProductModel"] = relationship(
        "ProductModel", back_populates="line_items"
    )
