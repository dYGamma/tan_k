# gui/product_manager.py
from PyQt5 import QtWidgets, QtCore
from services.product_service import ProductService
from gui.product_dialog import ProductDialog
import logging

logger = logging.getLogger(__name__)

class ProductManagerPage(QtWidgets.QWidget):
    data_changed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(8, 8, 8, 8)
        v.setSpacing(6)

        # Toolbar: поиск + CRUD
        toolbar = QtWidgets.QHBoxLayout()
        self.search = QtWidgets.QLineEdit()
        self.search.setPlaceholderText("🔍 Поиск по названию...")
        btn_add = QtWidgets.QPushButton("Добавить")
        btn_edit = QtWidgets.QPushButton("Редактировать")
        btn_delete = QtWidgets.QPushButton("Удалить")
        toolbar.addWidget(self.search, stretch=1)
        toolbar.addWidget(btn_add)
        toolbar.addWidget(btn_edit)
        toolbar.addWidget(btn_delete)
        v.addLayout(toolbar)

        # Таблица (ID, Название, Ед.изм., Срок (дн.), Остаток)
        self.table = QtWidgets.QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Ед.изм.", "Срок (дн.)", "Остаток"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        v.addWidget(self.table, stretch=1)

        # Сигналы
        self.search.textChanged.connect(self.reload)
        btn_add.clicked.connect(self.add_item)
        btn_edit.clicked.connect(self.edit_item)
        btn_delete.clicked.connect(self.delete_item)

        # Начальная загрузка
        self.reload()

    def reload(self):
        try:
            products = ProductService.list_all(filter_name=self.search.text())
        except Exception as e:
            logger.error("Ошибка загрузки списка товаров: %s", e, exc_info=True)
            products = []
        self.table.setRowCount(0)
        for p in products:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QtWidgets.QTableWidgetItem(str(p.id)))
            self.table.setItem(r, 1, QtWidgets.QTableWidgetItem(p.name))
            self.table.setItem(r, 2, QtWidgets.QTableWidgetItem(p.unit))
            self.table.setItem(r, 3, QtWidgets.QTableWidgetItem(str(p.expiration_days)))
            self.table.setItem(r, 4, QtWidgets.QTableWidgetItem(str(p.quantity)))

    def add_item(self):
        dlg = ProductDialog(parent=self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            name, unit, exp_days, qty = dlg.get_data()
            try:
                ProductService.create(name, unit, exp_days, quantity=qty)
                self.reload()
                self.data_changed.emit()
            except Exception as e:
                logger.error("Не удалось добавить товар: %s", e, exc_info=True)
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def edit_item(self):
        row = self.table.currentRow()
        if row < 0:
            return
        prod_id = int(self.table.item(row, 0).text())
        orig_name = self.table.item(row, 1).text()
        orig_unit = self.table.item(row, 2).text()
        orig_exp = int(self.table.item(row, 3).text())
        orig_qty = int(self.table.item(row, 4).text())
        dlg = ProductDialog(name=orig_name, unit=orig_unit, exp_days=orig_exp, qty=orig_qty, parent=self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            name, unit, exp_days, qty = dlg.get_data()
            try:
                ProductService.update(
                    prod_id,
                    name=name,
                    unit=unit,
                    expiration_days=exp_days,
                    quantity=qty
                )
                self.reload()
                self.data_changed.emit()
            except Exception as e:
                logger.error("Не удалось обновить товар: %s", e, exc_info=True)
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def delete_item(self):
        row = self.table.currentRow()
        if row < 0:
            return
        prod_id = int(self.table.item(row, 0).text())
        reply = QtWidgets.QMessageBox.question(
            self,
            "Подтвердите удаление",
            "Удалить товар?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply != QtWidgets.QMessageBox.Yes:
            return
        try:
            ProductService.delete(prod_id)
            self.reload()
            self.data_changed.emit()
        except Exception as e:
            logger.error("Не удалось удалить товар: %s", e, exc_info=True)
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))
