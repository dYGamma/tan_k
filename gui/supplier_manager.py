# gui/supplier_manager.py
from PyQt5 import QtWidgets, QtCore
from services.supplier_service import SupplierService
from gui.supplier_dialog import SupplierDialog
from services.session_manager import session_scope
from models.supplier import Supplier  # <<< Добавлен импорт
import logging

logger = logging.getLogger(__name__)

class SupplierRow:
    def __init__(self, table, row, supplier):
        self.table = table
        self.row = row
        self.id = supplier.id
        self.name = supplier.name
        self.contact = supplier.contact or ""

        self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(self.name))
        self.table.item(row, 0).setData(QtCore.Qt.UserRole, self.id)
        self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(self.contact))

class SupplierManagerPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)

        # Таблица поставщиков
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Название", "Контакты"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # Кнопки управления
        btn_layout = QtWidgets.QHBoxLayout()
        self.btn_add = QtWidgets.QPushButton("Добавить")
        self.btn_edit = QtWidgets.QPushButton("Редактировать")
        self.btn_delete = QtWidgets.QPushButton("Удалить")

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)

        # Подключение событий
        self.btn_add.clicked.connect(self.add_supplier)
        self.btn_edit.clicked.connect(self.edit_supplier)
        self.btn_delete.clicked.connect(self.delete_supplier)

        self.refresh_table()

    def refresh_table(self):
        suppliers = SupplierService.list_all()
        self.table.setRowCount(len(suppliers))
        for idx, supplier in enumerate(suppliers):
            SupplierRow(self.table, idx, supplier)

    def add_supplier(self):
        dlg = SupplierDialog(parent=self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            data = dlg.get_data()
            try:
                SupplierService.create(**data)
                self.refresh_table()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def edit_supplier(self):
        selected = self.table.selectedItems()
        if not selected:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите поставщика для редактирования")
            return

        row = selected[0].row()
        supplier_id = self.table.item(row, 0).data(QtCore.Qt.UserRole)
        with session_scope() as session:
            supplier = session.get(Supplier, supplier_id)
            if not supplier:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Поставщик не найден")
                return

            dlg = SupplierDialog(parent=self)
            dlg.e_name.setText(supplier.name)
            dlg.e_contact.setText(supplier.contact or "")
            if dlg.exec_() == QtWidgets.QDialog.Accepted:
                data = dlg.get_data()
                supplier.name = data["name"]
                supplier.contact = data["contact"]
                session.commit()
                self.refresh_table()

    def delete_supplier(self):
        selected = self.table.selectedItems()
        if not selected:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите поставщика для удаления")
            return

        row = selected[0].row()
        supplier_id = self.table.item(row, 0).data(QtCore.Qt.UserRole)
        reply = QtWidgets.QMessageBox.question(
            self, "Удаление", "Вы уверены, что хотите удалить поставщика?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            if SupplierService.delete(supplier_id):
                self.refresh_table()