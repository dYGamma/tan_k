# models/warehouse.py
from sqlalchemy import Column, Integer, String
from database import Base
import logging

logger = logging.getLogger(__name__)

class Warehouse(Base):
    __tablename__ = "warehouses"

    id       = Column(Integer, primary_key=True, index=True)
    name     = Column(String, nullable=False, unique=True, index=True)
    location = Column(String, nullable=True)

    def __repr__(self):
        return f"<Warehouse(id={self.id}, name={self.name}, location={self.location})>"
