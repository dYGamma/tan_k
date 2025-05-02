# gui/supplier_dialog.py
from PyQt5 import QtWidgets, QtCore

class SupplierDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить поставщика")
        self.setFixedSize(400, 200)

        layout = QtWidgets.QFormLayout(self)

        self.e_name = QtWidgets.QLineEdit()
        self.e_name.setPlaceholderText("Введите название поставщика")
        self.e_name.setObjectName("supplierNameInput")
        self.e_name.setToolTip("Уникальное название поставщика")

        self.e_contact = QtWidgets.QLineEdit()
        self.e_contact.setPlaceholderText("Контакты (опционально)")
        self.e_contact.setObjectName("supplierContactInput")
        self.e_contact.setToolTip("Телефон, email или адрес")

        layout.addRow("Название*", self.e_name)
        layout.addRow("Контакты", self.e_contact)

        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        btns.button(QtWidgets.QDialogButtonBox.Ok).setText("ОК")
        btns.button(QtWidgets.QDialogButtonBox.Cancel).setText("Отмена")
        btns.accepted.connect(self.validate_and_accept)
        btns.rejected.connect(self.reject)
        layout.addRow(btns)

    def validate_and_accept(self):
        name = self.e_name.text().strip()
        if not name:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите название поставщика")
            return
        self.accept()

    def get_data(self):
        return {
            'name': self.e_name.text().strip(),
            'contact': self.e_contact.text().strip() or None
        }