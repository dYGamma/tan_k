# models/product.py
from sqlalchemy import Column, Integer, String, Float, BigInteger, Index
from database import Base

class Product(Base):
    __tablename__ = "products"

    id                   = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name                 = Column(String(255), nullable=False, index=True)
    device_class         = Column(String(100), nullable=False, index=True)
    category             = Column(String(100), nullable=False, index=True)
    manufacturer         = Column(String(150), nullable=False, index=True)
    serial_number        = Column(String(100), nullable=False, unique=True)
    registration_number  = Column(String(100), nullable=False, unique=True)
    quantity             = Column(BigInteger, nullable=False, default=0)
    price                = Column(Float, nullable=False, default=0.0)

    __table_args__ = (
        Index("idx_name", "name"),
        Index("idx_device_class", "device_class"),
        Index("idx_category", "category"),
        Index("idx_manufacturer", "manufacturer"),
    )

    def __repr__(self):
        return (
            f"<Product(id={self.id}, name={self.name!r}, class={self.device_class!r}, "
            f"cat={self.category!r}, man={self.manufacturer!r}, ser={self.serial_number!r}, "
            f"reg={self.registration_number!r}, qty={self.quantity}, price={self.price})>"
        )
