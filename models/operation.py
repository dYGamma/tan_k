from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Operation(Base):
    __tablename__ = "operations"

    id          = Column(Integer, primary_key=True, index=True)
    product_id  = Column(Integer, ForeignKey("products.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    warehouse   = Column(String, nullable=False)
    quantity    = Column(Float, nullable=False)
    type        = Column(String, nullable=False)   # 'in'/'out'
    date        = Column(DateTime, default=datetime.utcnow, nullable=False)

    product  = relationship("Product")
    supplier = relationship("Supplier")
