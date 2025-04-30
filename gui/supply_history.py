# gui/supply_history.py
from PyQt5 import QtWidgets, QtCore
from services.operation_service import OperationService
from gui.operation_dialog import OperationDialog
import logging

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

        # Сигналы
        btn_add.clicked.connect(self.add_item)
        btn_edit.clicked.connect(self.edit_item)
        btn_delete.clicked.connect(self.delete_item)

        # Начальная загрузка
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
            self.table.setItem(r, 1, QtWidgets.QTableWidgetItem(op.product.name))
            self.table.setItem(r, 2, QtWidgets.QTableWidgetItem(op.supplier.name))
            self.table.setItem(r, 3, QtWidgets.QTableWidgetItem(op.warehouse))
            self.table.setItem(r, 4, QtWidgets.QTableWidgetItem(str(op.quantity)))
            self.table.setItem(r, 5, QtWidgets.QTableWidgetItem(op.type))
            self.table.setItem(r, 6, QtWidgets.QTableWidgetItem(op.date.strftime("%Y-%m-%d %H:%M:%S")))

    def add_item(self):
        dlg = OperationDialog(parent=self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            data = dlg.get_data()  # должен вернуть dict с keys: product_id, supplier_id, warehouse, quantity, op_type
            try:
                OperationService.create(
                    product_id=data['product_id'],
                    supplier_id=data['supplier_id'],
                    warehouse=data['warehouse'],
                    quantity=data['quantity'],
                    op_type=data['op_type']
                )
                self.reload()
                self.reload_request.emit()
            except Exception as e:
                logger.error("Не удалось добавить операцию: %s", e, exc_info=True)
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def edit_item(self):
        row = self.table.currentRow()
        if row < 0:
            return
        op_id = int(self.table.item(row, 0).text())
        current = {
            'product_id': None,
            'supplier_id': None,
            'warehouse': self.table.item(row, 3).text(),
            'quantity': int(self.table.item(row, 4).text()),
            'op_type': self.table.item(row, 5).text()
        }
        dlg = OperationDialog(**current, parent=self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            data = dlg.get_data()
            try:
                OperationService.update(
                    op_id,
                    product_id=data['product_id'],
                    supplier_id=data['supplier_id'],
                    warehouse=data['warehouse'],
                    quantity=data['quantity'],
                    op_type=data['op_type']
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
        reply = QtWidgets.QMessageBox.question(
            self,
            "Подтвердите удаление",
            "Удалить операцию?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply != QtWidgets.QMessageBox.Yes:
            return
        try:
            OperationService.delete(op_id)
            self.reload()
            self.reload_request.emit()
        except Exception as e:
            logger.error("Не удалось удалить операцию: %s", e, exc_info=True)
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))
