    # services/warehouse_service.py
import logging
from models.warehouse import Warehouse
from services.session_manager import session_scope

logger = logging.getLogger(__name__)

class WarehouseService:

    @staticmethod
    def list_all():
        """
        Возвращает все склады, упорядоченные по имени.
        """
        with session_scope() as s:
            return s.query(Warehouse).order_by(Warehouse.name).all()

    @staticmethod
    def create(name: str, location: str = None):
        """
        Создаёт новый склад.
        """
        if not name or not name.strip():
            raise ValueError("Название склада не может быть пустым")
        with session_scope() as s:
            w = Warehouse(name=name.strip(), location=(location or "").strip())
            s.add(w)
            logger.info("Warehouse '%s' created", name)
            return w

    @staticmethod
    def update(warehouse_id: int, name: str, location: str = None):
        """
        Обновляет склад по ID.
        """
        if not name or not name.strip():
            raise ValueError("Название склада не может быть пустым")
        with session_scope() as s:
            w = s.get(Warehouse, warehouse_id)
            if not w:
                return None
            w.name = name.strip()
            w.location = (location or "").strip()
            logger.info("Warehouse id=%d updated: name=%s", warehouse_id, name)
            return w

    @staticmethod
    def delete(warehouse_id: int):
        """
        Удаляет склад по ID.
        """
        with session_scope() as s:
            w = s.get(Warehouse, warehouse_id)
            if w:
                s.delete(w)
                logger.warning("Warehouse id=%d deleted", warehouse_id)
                return True
        return False
