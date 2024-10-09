from sqlalchemy import Column, Integer, String
from ..models.common_model import TimestampMixin, Base


class RestaurantModel(TimestampMixin, Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    logo = Column(String)
