# gui/product_manager.py
from PyQt5 import QtWidgets, QtCore
from services.product_service import ProductService
from gui.product_dialog import ProductDialog
from database import SessionLocal
from models.product import Product
import logging

logger = logging.getLogger(__name__)

class ProductManagerPage(QtWidgets.QWidget):
    data_changed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(8, 8, 8, 8)
        v.setSpacing(6)

        # Toolbar
        toolbar = QtWidgets.QHBoxLayout()
        self.search = QtWidgets.QLineEdit()
        self.search.setPlaceholderText("🔍 Поиск по названию или производителю...")
        btn_add = QtWidgets.QPushButton("Добавить")
        btn_edit = QtWidgets.QPushButton("Редактировать")
        btn_delete = QtWidgets.QPushButton("Удалить")
        toolbar.addWidget(self.search, stretch=1)
        toolbar.addWidget(btn_add)
        toolbar.addWidget(btn_edit)
        toolbar.addWidget(btn_delete)
        v.addLayout(toolbar)

        # Таблица
        headers = [
            "ID", "Название", "Класс", "Категория",
            "Производитель", "Сер. №", "Рег. №",
            "Кол-во", "Цена (₽)"
        ]
        self.table = QtWidgets.QTableWidget(0, len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        v.addWidget(self.table, stretch=1)

        # Сигналы
        self.search.textChanged.connect(self.reload)
        btn_add.clicked.connect(self.add_item)
        btn_edit.clicked.connect(self.edit_item)
        btn_delete.clicked.connect(self.delete_item)

        self.reload()

    def reload(self):
        try:
            products = ProductService.list_all(filter_name=self.search.text())
        except Exception as e:
            logger.error("Ошибка загрузки списка: %s", e, exc_info=True)
            products = []
        self.table.setRowCount(0)
        for p in products:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QtWidgets.QTableWidgetItem(str(p.id)))
            self.table.setItem(r, 1, QtWidgets.QTableWidgetItem(p.name))
            self.table.setItem(r, 2, QtWidgets.QTableWidgetItem(p.device_class))
            self.table.setItem(r, 3, QtWidgets.QTableWidgetItem(p.category))
            self.table.setItem(r, 4, QtWidgets.QTableWidgetItem(p.manufacturer))
            self.table.setItem(r, 5, QtWidgets.QTableWidgetItem(p.serial_number))
            self.table.setItem(r, 6, QtWidgets.QTableWidgetItem(p.registration_number))
            self.table.setItem(r, 7, QtWidgets.QTableWidgetItem(str(p.quantity)))
            self.table.setItem(r, 8, QtWidgets.QTableWidgetItem(f"{p.price:.2f}"))

    def add_item(self):
        dlg = ProductDialog(parent=self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            data = dlg.get_data()
            try:
                ProductService.create(**data)
                self.reload()
                self.data_changed.emit()
            except Exception as e:
                logger.error("Add failed: %s", e, exc_info=True)
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def edit_item(self):
        row = self.table.currentRow()
        if row < 0:
            return
        prod_id = int(self.table.item(row, 0).text())
        orig = {
            "name":               self.table.item(row, 1).text(),
            "device_class":       self.table.item(row, 2).text(),
            "category":           self.table.item(row, 3).text(),
            "manufacturer":       self.table.item(row, 4).text(),
            "serial_number":      self.table.item(row, 5).text(),
            "registration_number":self.table.item(row, 6).text(),
            "qty":                int(self.table.item(row, 7).text()),
            "price":              float(self.table.item(row, 8).text())
        }
        dlg = ProductDialog(**orig, parent=self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            data = dlg.get_data()
            try:
                ProductService.update(prod_id, **data)
                self.reload()
                self.data_changed.emit()
            except Exception as e:
                logger.error("Update failed: %s", e, exc_info=True)
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def delete_item(self):
        row = self.table.currentRow()
        if row < 0:
            return
        prod_id = int(self.table.item(row, 0).text())

        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle("Подтвердите удаление")
        msg_box.setText("Удалить изделие?")
        msg_box.setIcon(QtWidgets.QMessageBox.Question)
        yes_button = msg_box.addButton("Да", QtWidgets.QMessageBox.YesRole)
        no_button = msg_box.addButton("Нет", QtWidgets.QMessageBox.NoRole)
        msg_box.exec()

        if msg_box.clickedButton() != yes_button:
            return

        try:
            ProductService.delete(prod_id)
            self.reload()
            self.data_changed.emit()
        except Exception as e:
            logger.error("Delete failed: %s", e, exc_info=True)
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def get_total_count(self) -> int:
            """Возвращает общее число товаров в БД."""
            session = SessionLocal()
            try:
                return session.query(Product).count()
            finally:
                session.close()