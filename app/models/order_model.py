from sqlalchemy import Column, ForeignKey, Integer, String
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


class LineItemModel(TimestampMixin, Base):
    __tablename__ = "line_item"

    id = Column(Integer, primary_key=True)
    qyt_ordened = Column(Integer)
    comments = Column(String, nullable=True)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"))
    order_id = Column(Integer, ForeignKey("order.id", ondelete="CASCADE"))
