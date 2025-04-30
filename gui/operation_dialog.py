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
        """
        Диалог создания или редактирования операции прихода/расхода.

        :param product_id:      предварительно выбранный ID товара
        :param supplier_id:     предварительно выбранный ID поставщика
        :param warehouse_name:  имя склада для выбора по умолчанию
        :param quantity:        предварительное количество
        :param op_type:         'in' или 'out'
        :param parent:          родительский виджет
        """
        super().__init__(parent)
        self.setWindowTitle("Данные операции")
        self.setFixedSize(420, 260)

        form = QtWidgets.QFormLayout(self)
        form.setContentsMargins(12, 12, 12, 12)
        form.setSpacing(8)

        # Комбо-бокс товаров
        self.cb_product = QtWidgets.QComboBox()
        for p in ProductService.list_all():
            self.cb_product.addItem(f"{p.name} (ID:{p.id})", p.id)
        if product_id is not None:
            idx = self.cb_product.findData(product_id)
            if idx >= 0:
                self.cb_product.setCurrentIndex(idx)

        # Комбо-бокс поставщиков
        self.cb_supplier = QtWidgets.QComboBox()
        for s in SupplierService.list_all():
            self.cb_supplier.addItem(f"{s.name} (ID:{s.id})", s.id)
        if supplier_id is not None:
            idx = self.cb_supplier.findData(supplier_id)
            if idx >= 0:
                self.cb_supplier.setCurrentIndex(idx)

        # Комбо-бокс складов
        self.cb_warehouse = QtWidgets.QComboBox()
        for w in WarehouseService.list_all():
            self.cb_warehouse.addItem(f"{w.name} (ID:{w.id})", w.name)
        if warehouse_name:
            idx = self.cb_warehouse.findText(f"{warehouse_name} (ID:{self.cb_warehouse.currentData()})", QtCore.Qt.MatchStartsWith)
            # fallback: find by name only
            if idx == -1:
                for i in range(self.cb_warehouse.count()):
                    text = self.cb_warehouse.itemText(i)
                    if text.startswith(warehouse_name + " "):
                        idx = i
                        break
            if idx >= 0:
                self.cb_warehouse.setCurrentIndex(idx)

        # Поле количества
        self.s_quantity = QtWidgets.QDoubleSpinBox()
        self.s_quantity.setRange(0.0, 1e6)
        self.s_quantity.setDecimals(3)
        self.s_quantity.setValue(quantity)

        # Тип операции
        self.cb_type = QtWidgets.QComboBox()
        self.cb_type.addItems(['in', 'out'])
        if op_type in ('in', 'out'):
            self.cb_type.setCurrentText(op_type)

        form.addRow("Товар:", self.cb_product)
        form.addRow("Поставщик:", self.cb_supplier)
        form.addRow("Склад:", self.cb_warehouse)
        form.addRow("Количество:", self.s_quantity)
        form.addRow("Тип операции:", self.cb_type)

        # Кнопки
        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            parent=self
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        form.addRow(btns)

    def get_data(self):
        """
        Возвращает словарь:
            {
                'product_id': int,
                'supplier_id': int,
                'warehouse': str,
                'quantity': float,
                'op_type': str
            }
        """
        # Из текущего текста комбобокса склада берём всё до " (ID"
        wh_text = self.cb_warehouse.currentText()
        warehouse = wh_text.split(" (ID")[0] if " (ID" in wh_text else wh_text
        return {
            'product_id': self.cb_product.currentData(),
            'supplier_id': self.cb_supplier.currentData(),
            'warehouse': warehouse,
            'quantity': self.s_quantity.value(),
            'op_type': self.cb_type.currentText()
        }
