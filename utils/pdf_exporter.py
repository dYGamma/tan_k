# utils/pdf_exporter.py
import os
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from services.operation_service import OperationService
# Словарь для перевода типов
TYPE_MAP = {
    'in': 'Приход',
    'out': 'Расход'
}
# Путь до системных шрифтов (Windows) или шрифтов проекта
font_paths = {
    'Arial':       os.path.join(os.environ.get('WINDIR', 'C:\Windows'), 'Fonts', 'arial.ttf'),
    'Arial-Bold':  os.path.join(os.environ.get('WINDIR', 'C:\Windows'), 'Fonts', 'arialbd.ttf')
}
# Регистрируем шрифты с поддержкой кириллицы
for name, path in font_paths.items():
    if os.path.exists(path):
        pdfmetrics.registerFont(TTFont(name, path))


def export_inventory_pdf(path=None):
    """
    Генерирует PDF-отчёт по всем операциям.
    Возвращает количество записей.
    """
    if not path:
        path = f"inventory_{datetime.now():%Y%m%d_%H%M%S}.pdf"

    ops = OperationService.list_all()
    total = len(ops)

    # Заголовки и строки
    rows = [[
        "ID", "Товар", "Поставщик", "Склад",
        "Кол-во", "Тип", "Дата"
    ]]
    for op in ops:
        rows.append([
            op.id,
            op.product.name,
            op.supplier.name,
            op.warehouse,
            f"{op.quantity}",
            TYPE_MAP.get(op.type, op.type),
            op.date.strftime("%Y-%m-%d %H:%M:%S"),
        ])

    # Документ
    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        leftMargin=24, rightMargin=24,
        topMargin=36, bottomMargin=36
    )

    styles = getSampleStyleSheet()
    # Стиль заголовка
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        alignment=1,  # по центру
        fontName='Arial-Bold' if 'Arial-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold',
        fontSize=18,
        spaceAfter=12
    )
    # Обычный стиль
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['BodyText'],
        fontName='Arial' if 'Arial' in pdfmetrics.getRegisteredFontNames() else 'Helvetica',
        fontSize=10
    )

    elements = [
        Paragraph("Отчёт по инвентаризации", title_style),
        Spacer(1, 12),
    ]

    # Настройки ширины колонок (в пунктах)
    col_widths = [30, 140, 100, 60, 50, 50, 117]
    table = Table(rows, colWidths=col_widths, hAlign='CENTER', repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0), colors.HexColor('#4B4B4B')),
        ('TEXTCOLOR',     (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME',      (0, 0), (-1, 0), 'Arial-Bold'),
        ('FONTNAME',      (0, 1), (-1, -1), 'Arial'),
        ('FONTSIZE',      (0, 0), (-1, 0), 10),
        ('FONTSIZE',      (0, 1), (-1, -1), 9),
        ('GRID',          (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING',    (0, 0), (-1, 0), 8),
    ]))

    elements.append(table)

    doc.build(elements)
    return os.path.abspath(path)
