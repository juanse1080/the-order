from sqlalchemy import Column, ForeignKey, Integer, String
from ..models.common_model import TimestampMixin, Base


class ProductModel(TimestampMixin, Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
    description = Column(String, nullable=True)
    price = Column(Integer)

    restaurant_id = Column(Integer, ForeignKey("restaurant.id", ondelete="CASCADE"))
