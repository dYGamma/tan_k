# models/product.py
from sqlalchemy import Column, Integer, String
from database import Base
import logging

logger = logging.getLogger(__name__)

class Product(Base):
    __tablename__ = "products"

    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String, nullable=False, index=True)
    unit            = Column(String, nullable=False)
    expiration_days = Column(Integer, nullable=False)
    quantity        = Column(Integer, nullable=False, default=0)  # <<< Новое поле

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, unit={self.unit}, exp_days={self.expiration_days}, qty={self.quantity})>"
