# gui/warehouse_dialog.py
from PyQt5 import QtWidgets

class WarehouseDialog(QtWidgets.QDialog):
    def __init__(self, name: str = "", location: str = "", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Данные склада")
        self.setFixedSize(320, 180)

        form = QtWidgets.QFormLayout(self)
        form.setContentsMargins(12,12,12,12)
        form.setSpacing(8)

        self.edit_name = QtWidgets.QLineEdit(name)
        self.edit_location = QtWidgets.QLineEdit(location)

        form.addRow("Название склада:", self.edit_name)
        form.addRow("Расположение:", self.edit_location)

        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            parent=self
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        form.addRow(btns)

    def get_data(self) -> tuple:
        return (
            self.edit_name.text().strip(),
            self.edit_location.text().strip()
        )
