# services/operation_service.py
import logging
from models.operation import Operation
from services.session_manager import session_scope
from services.product_service import ProductService
from datetime import datetime
from sqlalchemy.orm import joinedload
from utils.data_validator import validate_positive_number, validate_nonempty

logger = logging.getLogger(__name__)

class OperationService:
    @staticmethod
    def list_all():
        """
        Возвращает список всех операций с предзагруженными связанными объектами.
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
        Создает новую операцию и автоматически корректирует остаток товара.
        
        Параметры:
            product_id: ID товара
            supplier_id: ID поставщика
            warehouse: название склада (не пустое)
            quantity: количество (>0)
            op_type: 'in' для прихода, 'out' для расхода
        """
        # Валидация
        if op_type not in ('in', 'out'):
            raise ValueError("Неверный тип операции (должен быть 'in' или 'out')")
        if not validate_nonempty(warehouse):
            raise ValueError("Поле 'склад' не может быть пустым")
        if not validate_positive_number(quantity):
            raise ValueError("Количество должно быть положительным числом")
        
        # Определяем дельту для остатка: + для прихода, – для расхода
        delta = quantity if op_type == 'in' else -quantity

        with session_scope() as s:
            try:
                # Корректируем остаток до сохранения операции,
                # чтобы в случае ошибки БД не было рассинхрона.
                ProductService.adjust_quantity(product_id, delta)

                op = Operation(
                    product_id=product_id,
                    supplier_id=supplier_id,
                    warehouse=warehouse,
                    quantity=quantity,
                    type=op_type,
                    date=datetime.utcnow()
                )
                s.add(op)
                s.flush()  # Получаем op.id до коммита
                
                logger.info(f"Operation {op_type} id={op.id} created, delta={delta}")
                return op
            except Exception as e:
                logger.error("Не удалось создать операцию: %s", e, exc_info=True)
                # В случае неудачи откатываем дельту
                try:
                    ProductService.adjust_quantity(product_id, -delta)
                except Exception:
                    logger.error("Не удалось откатить изменение остатка товара после ошибки операции", exc_info=True)
                raise

    @staticmethod
    def update(op_id: int, product_id: int, supplier_id: int,
               warehouse: str, quantity: float, op_type: str):
        """
        Обновляет существующую операцию,
        откатывая старое изменение остатка и применяя новое.
        
        Параметры:
            op_id: ID операции для редактирования
            далее — те же, что в create()
        """
        with session_scope() as s:
            op = s.get(Operation, op_id)
            if not op:
                return None

            # Валидация
            if op_type not in ('in', 'out'):
                raise ValueError("Неверный тип операции (должен быть 'in' или 'out')")
            if not validate_nonempty(warehouse):
                raise ValueError("Поле 'склад' не может быть пустым")
            if not validate_positive_number(quantity):
                raise ValueError("Количество должно быть положительным числом")

            # Откатываем старую дельту
            old_delta = op.quantity if op.type == 'in' else -op.quantity
            ProductService.adjust_quantity(op.product_id, -old_delta)

            # Применяем новые данные
            op.product_id = product_id
            op.supplier_id = supplier_id
            op.warehouse = warehouse
            op.quantity = quantity
            op.type = op_type
            op.date = datetime.utcnow()

            # Вычисляем и применяем новую дельту
            new_delta = quantity if op_type == 'in' else -quantity
            ProductService.adjust_quantity(product_id, new_delta)

            logger.info(f"Operation id={op_id} updated, old_delta={old_delta}, new_delta={new_delta}")
            return op

    @staticmethod
    def delete(op_id: int):
        """
        Удаляет операцию по ID и откатывает изменение остатка товара.
        """
        with session_scope() as s:
            op = s.get(Operation, op_id)
            if not op:
                return False

            # Откатываем дельту
            delta = op.quantity if op.type == 'in' else -op.quantity
            ProductService.adjust_quantity(op.product_id, -delta)

            s.delete(op)
            logger.warning(f"Operation id={op_id} deleted, rolled back delta={delta}")
            return True
