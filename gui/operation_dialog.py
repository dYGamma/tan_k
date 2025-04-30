# gui/operation_dialog.py
from PyQt5 import QtWidgets
from services.product_service import ProductService
from services.supplier_service import SupplierService

class OperationDialog(QtWidgets.QDialog):
    def __init__(self,
                 product_id=None, supplier_id=None,
                 warehouse="", quantity=0.0, op_type='in'):
        super().__init__()
        self.setWindowTitle("Данные операции")
        self.setFixedSize(400, 300)
        form = QtWidgets.QFormLayout(self)

        # Список продуктов
        self.cb_product = QtWidgets.QComboBox()
        products = ProductService.list_all()
        for p in products:
            self.cb_product.addItem(f"{p.name} (ID:{p.id})", p.id)
        if product_id:
            idx = self.cb_product.findData(product_id)
            if idx >= 0:
                self.cb_product.setCurrentIndex(idx)

        # Список поставщиков
        self.cb_supplier = QtWidgets.QComboBox()
        suppliers = SupplierService.list_all()
        for s in suppliers:
            self.cb_supplier.addItem(f"{s.name} (ID:{s.id})", s.id)
        if supplier_id:
            idx = self.cb_supplier.findData(supplier_id)
            if idx >= 0:
                self.cb_supplier.setCurrentIndex(idx)

        self.e_warehouse = QtWidgets.QLineEdit(warehouse)
        self.s_quantity = QtWidgets.QDoubleSpinBox()
        self.s_quantity.setRange(0.0, 1e6)
        self.s_quantity.setValue(quantity)
        self.cb_type = QtWidgets.QComboBox()
        self.cb_type.addItems(['in', 'out'])
        self.cb_type.setCurrentText(op_type)

        form.addRow("Продукт", self.cb_product)
        form.addRow("Поставщик", self.cb_supplier)
        form.addRow("Склад", self.e_warehouse)
        form.addRow("Количество", self.s_quantity)
        form.addRow("Тип операции", self.cb_type)

        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            parent=self
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        form.addRow(btns)

    def get_data(self):
        return {
            'product_id': self.cb_product.currentData(),
            'supplier_id': self.cb_supplier.currentData(),
            'warehouse': self.e_warehouse.text().strip(),
            'quantity': self.s_quantity.value(),
            'op_type': self.cb_type.currentText()
        }
