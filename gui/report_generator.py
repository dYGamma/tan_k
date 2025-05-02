# gui/report_generator.py
from PyQt5 import QtWidgets, QtCore
from utils.pdf_exporter import export_inventory_pdf
from utils.excel_exporter import export_inventory_excel
import logging
import os
import subprocess

logger = logging.getLogger(__name__)

class ReportPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)

        # --- Кнопки экспорта ---
        toolbar = QtWidgets.QHBoxLayout()
        toolbar.addStretch(1)
        self.btn_pdf   = QtWidgets.QPushButton("Экспорт в PDF")
        self.btn_excel = QtWidgets.QPushButton("Экспорт в Excel")
        toolbar.addWidget(self.btn_pdf)
        toolbar.addWidget(self.btn_excel)
        layout.addLayout(toolbar)

        # --- Статус ---
        self.status_lbl = QtWidgets.QLabel("")
        self.status_lbl.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.status_lbl)

        # Сигналы
        self.btn_pdf.clicked.connect(self.on_export_pdf)
        self.btn_excel.clicked.connect(self.on_export_excel)

    def _set_busy(self, busy: bool):
        for btn in (self.btn_pdf, self.btn_excel):
            btn.setDisabled(busy)
        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.WaitCursor if busy else QtCore.Qt.ArrowCursor
        )

    def _open_file(self, path: str):
        try:
            if os.name == 'nt':
                os.startfile(path)
            elif sys.platform == 'darwin':
                subprocess.call(('open', path))
            else:
                subprocess.call(('xdg-open', path))
        except Exception:
            logger.warning("Не удалось открыть файл автоматически: %s", path)

    def on_export_pdf(self):
        # Выбор файла для сохранения
        fn, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Сохранить PDF отчёт",
            None, "PDF files (*.pdf)"
        )
        if not fn:
            return

        self._set_busy(True)
        try:
            total = export_inventory_pdf(path=fn)
            self.status_lbl.setText(f"PDF-отчёт ({total} записей) сохранён:\n{fn}")
            logger.info("PDF report generated: %s (%d records)", fn, total)
            self._open_file(fn)
        except Exception as e:
            logger.error("Error exporting PDF: %s", e, exc_info=True)
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось создать PDF:\n{e}")
        finally:
            self._set_busy(False)

    def on_export_excel(self):
        # Выбор файла для сохранения
        fn, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Сохранить Excel отчёт",
            None, "Excel files (*.xlsx)"
        )
        if not fn:
            return

        self._set_busy(True)
        try:
            total = export_inventory_excel(path=fn)
            self.status_lbl.setText(f"Excel-отчёт ({total} записей) сохранён:\n{fn}")
            logger.info("Excel report generated: %s (%d records)", fn, total)
            self._open_file(fn)
        except Exception as e:
            logger.error("Error exporting Excel: %s", e, exc_info=True)
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось создать Excel:\n{e}")
        finally:
            self._set_busy(False)
