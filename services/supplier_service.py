import logging
from models.supplier import Supplier
from services.session_manager import session_scope

logger = logging.getLogger(__name__)

class SupplierService:

    @staticmethod
    def list_all():
        with session_scope() as s:
            return s.query(Supplier).order_by(Supplier.name).all()

    @staticmethod
    def create(name: str, contact: str):
        with session_scope() as s:
            sup = Supplier(name=name, contact=contact)
            s.add(sup)
            logger.info("Supplier '%s' created", name)
            return sup

    @staticmethod
    def delete(sup_id: int):
        with session_scope() as s:
            sup = s.get(Supplier, sup_id)
            if sup:
                s.delete(sup)
                logger.warning("Supplier id=%d deleted", sup_id)
                return True
        return False
