# services/product_service.py
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import SessionLocal
from models.product import Product

logger = logging.getLogger(__name__)

class ProductService:
    @staticmethod
    def list_all(filter_name: str = "") -> list[Product]:
        session: Session = SessionLocal()
        try:
            q = session.query(Product)
            if filter_name:
                pattern = f"%{filter_name}%"
                q = q.filter(
                    Product.name.ilike(pattern) |
                    Product.manufacturer.ilike(pattern)
                )
            return q.order_by(Product.id).all()
        except SQLAlchemyError as e:
            logger.error("list_all failed: %s", e, exc_info=True)
            return []
        finally:
            session.close()

    @staticmethod
    def create(
        name: str,
        device_class: str,
        category: str,
        manufacturer: str,
        serial_number: str,
        registration_number: str,
        quantity: int,
        price: float
    ) -> Product:
        session: Session = SessionLocal()
        try:
            prod = Product(
                name=name,
                device_class=device_class,
                category=category,
                manufacturer=manufacturer,
                serial_number=serial_number,
                registration_number=registration_number,
                quantity=quantity,
                price=price
            )
            session.add(prod)
            session.commit()
            session.refresh(prod)
            return prod
        except SQLAlchemyError as e:
            session.rollback()
            logger.error("create failed: %s", e, exc_info=True)
            raise
        finally:
            session.close()

    @staticmethod
    def update(
        prod_id: int,
        name: str,
        device_class: str,
        category: str,
        manufacturer: str,
        serial_number: str,
        registration_number: str,
        quantity: int,
        price: float
    ) -> Product:
        session: Session = SessionLocal()
        try:
            prod = session.get(Product, prod_id)
            if not prod:
                raise ValueError(f"Product with id={prod_id} not found")
            prod.name                 = name
            prod.device_class         = device_class
            prod.category             = category
            prod.manufacturer         = manufacturer
            prod.serial_number        = serial_number
            prod.registration_number  = registration_number
            prod.quantity             = quantity
            prod.price                = price

            session.commit()
            session.refresh(prod)
            return prod
        except SQLAlchemyError as e:
            session.rollback()
            logger.error("update failed: %s", e, exc_info=True)
            raise
        finally:
            session.close()

    @staticmethod
    def delete(prod_id: int) -> None:
        session: Session = SessionLocal()
        try:
            prod = session.get(Product, prod_id)
            if not prod:
                raise ValueError(f"Product with id={prod_id} not found")
            session.delete(prod)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.error("delete failed: %s", e, exc_info=True)
            raise
        finally:
            session.close()

    @staticmethod
    def adjust_quantity(prod_id: int, delta: int) -> Product:
        """
        Изменяет количество изделия на delta (может быть положительным или отрицательным).
        Возвращает обновлённый объект Product.
        """
        session: Session = SessionLocal()
        try:
            prod = session.get(Product, prod_id)
            if not prod:
                raise ValueError(f"Product with id={prod_id} not found")
            prod.quantity += delta
            if prod.quantity < 0:
                raise ValueError("Остаток не может быть отрицательным")
            session.commit()
            session.refresh(prod)
            return prod
        except SQLAlchemyError as e:
            session.rollback()
            logger.error("adjust_quantity failed: %s", e, exc_info=True)
            raise
        finally:
            session.close()
