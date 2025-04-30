# services/operation_service.py
import logging
from models.operation import Operation
from services.session_manager import session_scope
from datetime import datetime
from sqlalchemy.orm import joinedload

logger = logging.getLogger(__name__)

class OperationService:
    @staticmethod
    def list_all():
        """
        Возвращает список всех операций с предзагруженными связанными объектами
        """
        with session_scope() as s:
            return (
                s.query(Operation)
                .options(
                    joinedload(Operation.product),
                    joinedload(Operation.supplier)
                )
                .order_by(Operation.date.desc())
                .all()
            )

    @staticmethod
    def create(product_id: int, supplier_id: int,
               warehouse: str, quantity: float, op_type: str):
        """
        Создает новую операцию с валидацией данных
        """
        from utils.data_validator import validate_positive_number, validate_nonempty
        
        if op_type == 'out' and quantity <= 0:
            raise ValueError("Количество должно быть > 0 для операции расхода")
            
        if not validate_nonempty(warehouse) or not validate_positive_number(quantity):
            raise ValueError("Неверные данные операции")

        with session_scope() as s:
            try:
                op = Operation(
                    product_id=product_id,
                    supplier_id=supplier_id,
                    warehouse=warehouse,
                    quantity=quantity,
                    type=op_type,
                    date=datetime.utcnow()
                )
                s.add(op)
                s.flush()  # Получаем ID до коммита
                
                # Безопасное логирование без использования %d
                logger.info(f"Operation {op_type} id={op.id} created")
                
                return op
            except Exception as e:
                logger.error("Не удалось создать операцию: %s", str(e), exc_info=True)
                raise

    @staticmethod
    def update(op_id: int, **kwargs):
        """
        Обновляет существующую операцию
        """
        with session_scope() as s:
            op = s.get(Operation, op_id)
            if not op:
                return None
                
            for key, value in kwargs.items():
                setattr(op, key, value)
                
            logger.info(f"Operation id={op_id} updated")
            return op

    @staticmethod
    def delete(op_id: int):
        """
        Удаляет операцию по ID
        """
        with session_scope() as s:
            op = s.get(Operation, op_id)
            if op:
                s.delete(op)
                logger.warning(f"Operation id={op_id} deleted")
                return True
            return False