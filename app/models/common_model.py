from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class TimestampMixin(object):
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
