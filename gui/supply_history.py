# gui/supply_history.py
from PyQt5 import QtWidgets, QtCore
from services.operation_service import OperationService
from gui.operation_dialog import OperationDialog
from database import SessionLocal
from models.operation import Operation
import logging
import re

logger = logging.getLogger(__name__)

class OperationPage(QtWidgets.QWidget):
    reload_request = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(8, 8, 8, 8)
        v.setSpacing(6)

        # Toolbar: CRUD
        toolbar = QtWidgets.QHBoxLayout()
        btn_add = QtWidgets.QPushButton("Добавить операцию")
        btn_edit = QtWidgets.QPushButton("Редактировать")
        btn_delete = QtWidgets.QPushButton("Удалить")
        toolbar.addWidget(btn_add)
        toolbar.addWidget(btn_edit)
        toolbar.addWidget(btn_delete)
        toolbar.addStretch()
        v.addLayout(toolbar)

        # Таблица операций
        self.table = QtWidgets.QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Товар", "Поставщик", "Склад", "Кол-во", "Тип", "Дата"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        v.addWidget(self.table, stretch=1)

        btn_add.clicked.connect(self.add_item)
        btn_edit.clicked.connect(self.edit_item)
        btn_delete.clicked.connect(self.delete_item)

        self.reload()

    def reload(self):
        try:
            ops = OperationService.list_all()
        except Exception as e:
            logger.error("Ошибка загрузки операций: %s", e, exc_info=True)
            ops = []
        self.table.setRowCount(0)
        for op in ops:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QtWidgets.QTableWidgetItem(str(op.id)))
            self.table.setItem(r, 1, QtWidgets.QTableWidgetItem(f"{op.product.name} (ID:{op.product.id})"))
            self.table.setItem(r, 2, QtWidgets.QTableWidgetItem(f"{op.supplier.name} (ID:{op.supplier.id})"))
            self.table.setItem(r, 3, QtWidgets.QTableWidgetItem(op.warehouse))
            self.table.setItem(r, 4, QtWidgets.QTableWidgetItem(str(op.quantity)))
            # Показать Приход/Расход вместо in/out
            typ = "Приход" if op.type == "in" else "Расход"
            self.table.setItem(r, 5, QtWidgets.QTableWidgetItem(typ))
            self.table.setItem(r, 6, QtWidgets.QTableWidgetItem(op.date.strftime("%Y-%m-%d %H:%M:%S")))

    def add_item(self):
        dlg = OperationDialog(parent=self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            data = dlg.get_data()
            try:
                OperationService.create(**data)
                self.reload()
                self.reload_request.emit()
            except Exception as e:
                logger.error("Не удалось добавить операцию: %s", e, exc_info=True)
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def edit_item(self):
        row = self.table.currentRow()
        if row < 0:
            return

        # Парсер ID из текста "Name (ID:123)"
        def parse_id(text):
            m = re.search(r"ID:(\d+)", text)
            return int(m.group(1)) if m else None

        current = {
            'product_id':     parse_id(self.table.item(row, 1).text()),
            'supplier_id':    parse_id(self.table.item(row, 2).text()),
            'warehouse_name': self.table.item(row, 3).text(),
            'quantity':       float(self.table.item(row, 4).text()),
            'op_type':        'in' if self.table.item(row, 5).text() == "Приход" else 'out'
        }

        dlg = OperationDialog(**current, parent=self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            data = dlg.get_data()
            try:
                OperationService.update(
                    int(self.table.item(row, 0).text()),
                    **data
                )
                self.reload()
                self.reload_request.emit()
            except Exception as e:
                logger.error("Не удалось обновить операцию: %s", e, exc_info=True)
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def delete_item(self):
        row = self.table.currentRow()
        if row < 0:
            return
        op_id = int(self.table.item(row, 0).text())

        mb = QtWidgets.QMessageBox(self)
        mb.setIcon(QtWidgets.QMessageBox.Question)
        mb.setWindowTitle("Подтвердите удаление")
        mb.setText("Удалить операцию?")
        btn_yes = mb.addButton("Да", QtWidgets.QMessageBox.YesRole)
        btn_no  = mb.addButton("Нет", QtWidgets.QMessageBox.NoRole)
        mb.setDefaultButton(btn_no)
        mb.exec_()

        if mb.clickedButton() != btn_yes:
            return

        try:
            OperationService.delete(op_id)
            self.reload()
            self.reload_request.emit()
        except Exception as e:
            logger.error("Не удалось удалить операцию: %s", e, exc_info=True)
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def get_total_count(self) -> int:
        """Возвращает общее число операций."""
        session = SessionLocal()
        try:
            return session.query(Operation).count()
        finally:
            session.close()