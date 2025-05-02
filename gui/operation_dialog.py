# gui/operation_dialog.py
from PyQt5 import QtWidgets, QtCore
from services.product_service import ProductService
from services.supplier_service import SupplierService
from services.warehouse_service import WarehouseService

class OperationDialog(QtWidgets.QDialog):
    def __init__(
        self,
        product_id=None,
        supplier_id=None,
        warehouse_name="",
        quantity=0.0,
        op_type='in',
        parent=None
    ):
        super().__init__(parent)
        self.setWindowTitle("Данные операции")
        self.setFixedSize(420, 260)

        form = QtWidgets.QFormLayout(self)
        form.setContentsMargins(12, 12, 12, 12)
        form.setSpacing(8)

        # Товар
        self.cb_product = QtWidgets.QComboBox()
        for p in ProductService.list_all():
            self.cb_product.addItem(f"{p.name} (ID:{p.id})", p.id)
        if product_id is not None:
            idx = self.cb_product.findData(product_id)
            if idx >= 0:
                self.cb_product.setCurrentIndex(idx)

        # Поставщик
        self.cb_supplier = QtWidgets.QComboBox()
        for s in SupplierService.list_all():
            self.cb_supplier.addItem(f"{s.name} (ID:{s.id})", s.id)
        if supplier_id is not None:
            idx = self.cb_supplier.findData(supplier_id)
            if idx >= 0:
                self.cb_supplier.setCurrentIndex(idx)

        # Склад
        self.cb_warehouse = QtWidgets.QComboBox()
        for w in WarehouseService.list_all():
            self.cb_warehouse.addItem(w.name, w.name)
        if warehouse_name:
            idx = self.cb_warehouse.findText(warehouse_name, QtCore.Qt.MatchExactly)
            if idx >= 0:
                self.cb_warehouse.setCurrentIndex(idx)

        # Количество
        self.s_quantity = QtWidgets.QDoubleSpinBox()
        self.s_quantity.setRange(0.0, 1e6)
        self.s_quantity.setDecimals(3)
        self.s_quantity.setValue(quantity)

        # Тип операции: Приход/Расход
        self.cb_type = QtWidgets.QComboBox()
        self.cb_type.addItem("Приход", "in")
        self.cb_type.addItem("Расход", "out")
        idx = self.cb_type.findData(op_type)
        if idx >= 0:
            self.cb_type.setCurrentIndex(idx)

        form.addRow("Товар:", self.cb_product)
        form.addRow("Поставщик:", self.cb_supplier)
        form.addRow("Склад:", self.cb_warehouse)
        form.addRow("Количество:", self.s_quantity)
        form.addRow("Тип операции:", self.cb_type)

        # Кнопки ОК/Отмена на русском
        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            parent=self
        )
        # Переименовываем кнопки:
        ok_btn = btns.button(QtWidgets.QDialogButtonBox.Ok)
        ok_btn.setText("ОК")
        cancel_btn = btns.button(QtWidgets.QDialogButtonBox.Cancel)
        cancel_btn.setText("Отмена")

        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        form.addRow(btns)

    def get_data(self):
        return {
            'product_id':   self.cb_product.currentData(),
            'supplier_id':  self.cb_supplier.currentData(),
            'warehouse':    self.cb_warehouse.currentData(),
            'quantity':     self.s_quantity.value(),
            'op_type':      self.cb_type.currentData()
        }
