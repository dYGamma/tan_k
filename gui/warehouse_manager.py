# gui/warehouse_manager.py
from PyQt5 import QtWidgets, QtCore
from services.warehouse_service import WarehouseService
from gui.warehouse_dialog import WarehouseDialog
import logging

logger = logging.getLogger(__name__)

class WarehouseManagerPage(QtWidgets.QWidget):
    data_changed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(8,8,8,8)
        v.setSpacing(6)

        # Toolbar
        toolbar = QtWidgets.QHBoxLayout()
        btn_add    = QtWidgets.QPushButton("Добавить склад")
        btn_edit   = QtWidgets.QPushButton("Редактировать")
        btn_delete = QtWidgets.QPushButton("Удалить")
        toolbar.addWidget(btn_add)
        toolbar.addWidget(btn_edit)
        toolbar.addWidget(btn_delete)
        toolbar.addStretch()
        v.addLayout(toolbar)

        # Таблица складов
        self.table = QtWidgets.QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Расположение"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        v.addWidget(self.table, stretch=1)

        # Сигналы
        btn_add.clicked.connect(self.add_item)
        btn_edit.clicked.connect(self.edit_item)
        btn_delete.clicked.connect(self.delete_item)

        # Загрузка данных
        self.reload()

    def reload(self):
        try:
            warehouses = WarehouseService.list_all()
        except Exception as e:
            logger.error("Ошибка загрузки складов: %s", e, exc_info=True)
            warehouses = []
        self.table.setRowCount(0)
        for w in warehouses:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QtWidgets.QTableWidgetItem(str(w.id)))
            self.table.setItem(r, 1, QtWidgets.QTableWidgetItem(w.name))
            self.table.setItem(r, 2, QtWidgets.QTableWidgetItem(w.location or ""))

    def add_item(self):
        dlg = WarehouseDialog(parent=self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            name, location = dlg.get_data()
            try:
                WarehouseService.create(name, location)
                self.reload()
                self.data_changed.emit()
            except Exception as e:
                logger.error("Не удалось добавить склад: %s", e, exc_info=True)
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def edit_item(self):
        row = self.table.currentRow()
        if row < 0:
            return
        wh_id = int(self.table.item(row, 0).text())
        orig_name = self.table.item(row, 1).text()
        orig_loc  = self.table.item(row, 2).text()
        dlg = WarehouseDialog(name=orig_name, location=orig_loc, parent=self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            name, location = dlg.get_data()
            try:
                WarehouseService.update(wh_id, name, location)
                self.reload()
                self.data_changed.emit()
            except Exception as e:
                logger.error("Не удалось обновить склад: %s", e, exc_info=True)
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def delete_item(self):
        row = self.table.currentRow()
        if row < 0:
            return
        wh_id = int(self.table.item(row, 0).text())
        reply = QtWidgets.QMessageBox.question(
            self, "Подтвердите удаление", "Удалить склад?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply != QtWidgets.QMessageBox.Yes:
            return
        try:
            WarehouseService.delete(wh_id)
            self.reload()
            self.data_changed.emit()
        except Exception as e:
            logger.error("Не удалось удалить склад: %s", e, exc_info=True)
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))
