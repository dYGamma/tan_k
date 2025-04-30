# gui/product_dialog.py
from PyQt5 import QtWidgets

class ProductDialog(QtWidgets.QDialog):
    def __init__(
        self,
        name: str = "",
        unit: str = "",
        exp_days: int = 0,
        qty: int = 0,
        parent=None
    ):
        """
        Диалог создания/редактирования товара.

        Аргументы:
            name     — текущее название (или "" для нового)
            unit     — текущая единица измерения
            exp_days — текущий срок годности (дней)
            qty      — текущий остаток
            parent   — родительский виджет
        """
        super().__init__(parent)
        self.setWindowTitle("Данные товара")
        self.setFixedSize(360, 220)

        form = QtWidgets.QFormLayout(self)
        form.setContentsMargins(12, 12, 12, 12)
        form.setSpacing(8)

        # Поля ввода
        self.edit_name = QtWidgets.QLineEdit(name)
        self.edit_unit = QtWidgets.QLineEdit(unit)

        self.spin_exp = QtWidgets.QSpinBox()
        self.spin_exp.setRange(0, 3650)
        self.spin_exp.setValue(exp_days)

        self.spin_qty = QtWidgets.QSpinBox()
        self.spin_qty.setRange(0, 10**9)
        self.spin_qty.setValue(qty)

        # Собираем форму
        form.addRow("Название:", self.edit_name)
        form.addRow("Ед. изм.:", self.edit_unit)
        form.addRow("Срок годности (дн.):", self.spin_exp)
        form.addRow("Остаток:", self.spin_qty)

        # Кнопки ОК/Отмена
        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            parent=self
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        form.addRow(btns)

    def get_data(self) -> tuple:
        """
        Возвращает кортеж:
            (name: str, unit: str, expiration_days: int, quantity: int)
        """
        return (
            self.edit_name.text().strip(),
            self.edit_unit.text().strip(),
            self.spin_exp.value(),
            self.spin_qty.value(),
        )
