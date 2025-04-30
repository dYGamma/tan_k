# services/product_service.py
import logging
from models.product import Product
from services.session_manager import session_scope

logger = logging.getLogger(__name__)

class ProductService:

    @staticmethod
    def list_all(filter_name: str = None):
        """
        Возвращает список всех товаров, при необходимости фильтруя по названию.
        """
        with session_scope() as s:
            q = s.query(Product)
            if filter_name:
                q = q.filter(Product.name.ilike(f"%{filter_name}%"))
            return q.order_by(Product.name).all()

    @staticmethod
    def create(name: str, unit: str, exp_days: int, quantity: int = 0):
        """
        Создаёт новый товар с начальным количеством quantity.
        """
        from utils.data_validator import validate_product
        if not validate_product(name, unit, exp_days) or quantity < 0:
            raise ValueError("Invalid product data or negative quantity")
        with session_scope() as s:
            p = Product(
                name=name,
                unit=unit,
                expiration_days=exp_days,
                quantity=quantity
            )
            s.add(p)
            logger.info("Product '%s' created with quantity=%d", name, quantity)
            return p

    @staticmethod
    def update(prod_id: int, **kwargs):
        """
        Обновляет поля товара. Можно передать name, unit, expiration_days, quantity.
        """
        with session_scope() as s:
            p = s.get(Product, prod_id)
            if not p:
                logger.warning("Product id=%d not found for update", prod_id)
                return None
            if 'quantity' in kwargs and kwargs['quantity'] < 0:
                raise ValueError("Quantity cannot be negative")
            for k, v in kwargs.items():
                setattr(p, k, v)
            logger.info("Product id=%d updated: %s", prod_id, kwargs)
            return p

    @staticmethod
    def delete(prod_id: int):
        """
        Удаляет товар по его ID.
        """
        with session_scope() as s:
            p = s.get(Product, prod_id)
            if p:
                s.delete(p)
                logger.warning("Product id=%d deleted", prod_id)
                return True
        logger.warning("Product id=%d not found for deletion", prod_id)
        return False

    @staticmethod
    def adjust_quantity(prod_id: int, delta: int):
        """
        Изменяет количество товара на складе на delta (может быть отрицательным).
        """
        with session_scope() as s:
            p = s.get(Product, prod_id)
            if not p:
                logger.error("Product id=%d not found for quantity adjustment", prod_id)
                return None
            new_qty = p.quantity + delta
            if new_qty < 0:
                raise ValueError(f"Insufficient stock for product id={prod_id}")
            p.quantity = new_qty
            logger.info("Product id=%d quantity adjusted by %d, new quantity=%d", prod_id, delta, new_qty)
            return p
