import xlsxwriter
from services.operation_service import OperationService
from datetime import datetime

def export_inventory_excel(path=None):
    if not path:
        path = f"inventory_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
    ops = OperationService.list_all()
    workbook = xlsxwriter.Workbook(path)
    sheet = workbook.add_worksheet("Inventory")

    headers = ["ID","Product","Supplier","Warehouse","Quantity","Type","Date"]
    sheet.write_row(0, 0, headers)

    for idx, op in enumerate(ops, start=1):
        row = [
            op.id,
            op.product.name,
            op.supplier.name,
            op.warehouse,
            op.quantity,
            op.type,
            op.date.strftime("%Y-%m-%d %H:%M:%S"),
        ]
        sheet.write_row(idx, 0, row)

    workbook.close()
    return path
