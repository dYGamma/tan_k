# gui/product_dialog.py
from PyQt5 import QtWidgets

class ProductDialog(QtWidgets.QDialog):
    def __init__(
        self,
        name: str = "",
        device_class: str = "",
        category: str = "",
        manufacturer: str = "",
        serial_number: str = "",
        registration_number: str = "",
        qty: int = 0,
        price: float = 0.0,
        parent=None
    ):
        super().__init__(parent)
        self.setWindowTitle("Данные изделия")
        self.setFixedSize(400, 350)

        form = QtWidgets.QFormLayout(self)
        form.setContentsMargins(12, 12, 12, 12)
        form.setSpacing(8)

        self.edit_name = QtWidgets.QLineEdit(name)
        self.edit_class = QtWidgets.QLineEdit(device_class)
        self.edit_cat   = QtWidgets.QLineEdit(category)
        self.edit_man   = QtWidgets.QLineEdit(manufacturer)
        self.edit_ser   = QtWidgets.QLineEdit(serial_number)
        self.edit_reg   = QtWidgets.QLineEdit(registration_number)

        self.spin_qty = QtWidgets.QSpinBox()
        self.spin_qty.setRange(0, 10**9)
        self.spin_qty.setValue(qty)

        self.spin_price = QtWidgets.QDoubleSpinBox()
        self.spin_price.setRange(0, 1e9)
        self.spin_price.setDecimals(2)
        self.spin_price.setValue(price)

        form.addRow("Название:", self.edit_name)
        form.addRow("Класс изделия:", self.edit_class)
        form.addRow("Категория:", self.edit_cat)
        form.addRow("Производитель:", self.edit_man)
        form.addRow("Серийный №:", self.edit_ser)
        form.addRow("Рег. №:", self.edit_reg)
        form.addRow("Количество:", self.spin_qty)
        form.addRow("Цена (₽):", self.spin_price)

        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            parent=self
        )

        btns.button(QtWidgets.QDialogButtonBox.Ok).setText("ОК")
        btns.button(QtWidgets.QDialogButtonBox.Cancel).setText("Отмена")

        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        form.addRow(btns)

    def get_data(self) -> dict:
        return {
            "name":               self.edit_name.text().strip(),
            "device_class":       self.edit_class.text().strip(),
            "category":           self.edit_cat.text().strip(),
            "manufacturer":       self.edit_man.text().strip(),
            "serial_number":      self.edit_ser.text().strip(),
            "registration_number":self.edit_reg.text().strip(),
            "quantity":           self.spin_qty.value(),
            "price":              self.spin_price.value(),
        }
