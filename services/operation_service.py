import logging
from models.operation import Operation
from services.session_manager import session_scope
from datetime import datetime

logger = logging.getLogger(__name__)

class OperationService:

    @staticmethod
    def list_all():
        with session_scope() as s:
            return s.query(Operation).order_by(Operation.date.desc()).all()

    @staticmethod
    def create(product_id: int, supplier_id: int,
               warehouse: str, quantity: float, op_type: str):
        from utils.data_validator import validate_positive_number, validate_nonempty
        if op_type == 'out' and quantity <= 0:
            raise ValueError("Quantity must be > 0 for 'out'")
        if not validate_nonempty(warehouse) or not validate_positive_number(quantity):
            raise ValueError("Invalid operation data")
        with session_scope() as s:
            op = Operation(
                product_id=product_id,
                supplier_id=supplier_id,
                warehouse=warehouse,
                quantity=quantity,
                type=op_type,
                date=datetime.utcnow()
            )
            s.add(op)
            logger.info("Operation %s id=%d created", op_type, op.id)
            return op

    @staticmethod
    def update(op_id: int, **kwargs):
        with session_scope() as s:
            op = s.get(Operation, op_id)
            if not op:
                return None
            for k, v in kwargs.items():
                setattr(op, k, v)
            logger.info("Operation id=%d updated", op_id)
            return op

    @staticmethod
    def delete(op_id: int):
        with session_scope() as s:
            op = s.get(Operation, op_id)
            if op:
                s.delete(op)
                logger.warning("Operation id=%d deleted", op_id)
                return True
        return False
