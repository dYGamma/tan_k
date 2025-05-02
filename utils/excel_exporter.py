# utils/excel_exporter.py
import xlsxwriter
from services.operation_service import OperationService
from datetime import datetime

# Словарь для перевода типов
TYPE_MAP = {
    'in': 'Приход',
    'out': 'Расход'
}

def export_inventory_excel(path=None):
    """
    Генерирует Excel-отчёт по операциям.
    Возвращает количество записей.
    """
    if not path:
        path = f"inventory_{datetime.now():%Y%m%d_%H%M%S}.xlsx"

    ops = OperationService.list_all()

    workbook = xlsxwriter.Workbook(path)
    sheet = workbook.add_worksheet("Inventory")

    # Заголовки
    headers = ["ID","Товар","Поставщик","Склад","Кол-во","Тип","Дата"]
    sheet.write_row(0, 0, headers)

    # Данные
    for idx, op in enumerate(ops, start=1):
        row = [
            op.id,
            op.product.name,
            op.supplier.name,
            op.warehouse,
            op.quantity,
            TYPE_MAP.get(op.type, op.type),  # тут переводим
            op.date.strftime("%Y-%m-%d %H:%M:%S"),
        ]
        sheet.write_row(idx, 0, row)

    workbook.close()
    return len(ops)
