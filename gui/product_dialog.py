# gui/product_dialog.py
from PyQt5 import QtWidgets

class ProductDialog(QtWidgets.QDialog):
    def __init__(self, name="", unit="", exp=0):
        super().__init__()
        self.setWindowTitle("Данные товара")
        self.setFixedSize(320, 180)
        form = QtWidgets.QFormLayout(self)

        self.e_name = QtWidgets.QLineEdit(name)
        self.e_unit = QtWidgets.QLineEdit(unit)
        self.s_exp = QtWidgets.QSpinBox()
        self.s_exp.setRange(0, 365)
        self.s_exp.setValue(exp)

        form.addRow("Название", self.e_name)
        form.addRow("Ед.изм.", self.e_unit)
        form.addRow("Срок (дн.)", self.s_exp)

        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            parent=self
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        form.addRow(btns)

    def get_data(self):
        return (
            self.e_name.text().strip(),
            self.e_unit.text().strip(),
            self.s_exp.value()
        )
