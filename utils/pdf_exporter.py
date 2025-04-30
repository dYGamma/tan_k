from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from services.operation_service import OperationService
import os
from datetime import datetime

def export_inventory_pdf(path=None):
    if not path:
        path = f"inventory_{datetime.now():%Y%m%d_%H%M%S}.pdf"
    ops = OperationService.list_all()
    rows = [
        ["ID","Product","Supplier","Warehouse","Quantity","Type","Date"]
    ]
    for op in ops:
        rows.append([
            op.id,
            op.product.name,
            op.supplier.name,
            op.warehouse,
            op.quantity,
            op.type,
            op.date.strftime("%Y-%m-%d %H:%M:%S"),
        ])
    doc = SimpleDocTemplate(path, pagesize=A4)
    style = getSampleStyleSheet()
    elements = [
        Paragraph("Inventory Report", style["Title"]),
        Table(rows, hAlign='LEFT')
    ]
    doc.build(elements)
    return os.path.abspath(path)
