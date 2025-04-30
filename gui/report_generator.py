# gui/report_generator.py
from PyQt5 import QtWidgets, QtCore
from utils.pdf_exporter import export_inventory_pdf
from utils.excel_exporter import export_inventory_excel
import logging

logger = logging.getLogger(__name__)

class ReportPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)

        toolbar = QtWidgets.QHBoxLayout()
        toolbar.addStretch(1)
        self.btn_pdf = QtWidgets.QPushButton("Экспорт в PDF")
        self.btn_excel = QtWidgets.QPushButton("Экспорт в Excel")
        toolbar.addWidget(self.btn_pdf)
        toolbar.addWidget(self.btn_excel)
        layout.addLayout(toolbar)

        self.status_lbl = QtWidgets.QLabel("")
        self.status_lbl.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.status_lbl)

        self.btn_pdf.clicked.connect(self.on_export_pdf)
        self.btn_excel.clicked.connect(self.on_export_excel)

    def on_export_pdf(self):
        try:
            path = export_inventory_pdf()
            logger.info("PDF report generated: %s", path)
            self.status_lbl.setText(f"PDF-отчёт сохранён: {path}")
        except Exception as e:
            logger.error("Error exporting PDF: %s", e, exc_info=True)
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Не удалось сформировать PDF")

    def on_export_excel(self):
        try:
            path = export_inventory_excel()
            logger.info("Excel report generated: %s", path)
            self.status_lbl.setText(f"Excel-отчёт сохранён: {path}")
        except Exception as e:
            logger.error("Error exporting Excel: %s", e, exc_info=True)
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Не удалось сформировать Excel")
