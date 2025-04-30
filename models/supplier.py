from sqlalchemy import Column, Integer, String
from database import Base
import logging

logger = logging.getLogger(__name__)

class Supplier(Base):
    __tablename__ = "suppliers"

    id      = Column(Integer, primary_key=True, index=True)
    name    = Column(String, nullable=False, unique=True)
    contact = Column(String)
