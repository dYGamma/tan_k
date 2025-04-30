import logging
from models.product import Product
from services.session_manager import session_scope

logger = logging.getLogger(__name__)

class ProductService:

    @staticmethod
    def list_all(filter_name: str = None):
        with session_scope() as s:
            q = s.query(Product)
            if filter_name:
                q = q.filter(Product.name.ilike(f"%{filter_name}%"))
            return q.order_by(Product.name).all()

    @staticmethod
    def create(name: str, unit: str, exp_days: int):
        from utils.data_validator import validate_product
        if not validate_product(name, unit, exp_days):
            raise ValueError("Invalid product data")
        with session_scope() as s:
            p = Product(name=name, unit=unit, expiration_days=exp_days)
            s.add(p)
            logger.info("Product '%s' created", name)
            return p

    @staticmethod
    def update(prod_id: int, **kwargs):
        with session_scope() as s:
            p = s.get(Product, prod_id)
            if not p:
                return None
            for k, v in kwargs.items():
                setattr(p, k, v)
            logger.info("Product id=%d updated", prod_id)
            return p

    @staticmethod
    def delete(prod_id: int):
        with session_scope() as s:
            p = s.get(Product, prod_id)
            if p:
                s.delete(p)
                logger.warning("Product id=%d deleted", prod_id)
                return True
        return False
