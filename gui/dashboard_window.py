# gui/dashboard_window.py
from PyQt5 import QtWidgets, QtCore
from utils.theme_manager import toggle_theme, update_theme_ui
from gui.product_manager import ProductManagerPage
from gui.supply_history import OperationPage
from gui.report_generator import ReportPage
from gui.role_manager import RoleManagerPage
from gui.supplier_manager import SupplierManagerPage  # <<< Новый импорт
import logging

logger = logging.getLogger(__name__)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, user, make_login_dialog):
        super().__init__()
        self.user = user
        self.make_login_dialog = make_login_dialog

        self.setWindowTitle(f"Inventory System — {user.role}")
        self.resize(1024, 768)

        # — Навигация слева
        self.nav_list = QtWidgets.QListWidget()
        self.nav_list.setFixedWidth(180)
        self.nav_list.addItem("📦 Товары")
        self.nav_list.addItem("🔄 Операции")
        self.nav_list.addItem("🚚 Поставщики")  # <<< Новая вкладка
        self.nav_list.addItem("📊 Отчёты")
        if user.role == "admin":
            self.nav_list.addItem("👥 Пользователи")
        self.nav_list.currentRowChanged.connect(self.on_nav_changed)

        # — Страницы
        self.stack = QtWidgets.QStackedWidget()
        self.product_page = ProductManagerPage()
        self.operation_page = OperationPage()
        self.supplier_page = SupplierManagerPage()  # <<< Новая страница
        self.report_page = ReportPage()
        self.stack.addWidget(self.product_page)
        self.stack.addWidget(self.operation_page)
        self.stack.addWidget(self.supplier_page)  # <<< Добавлена
        self.stack.addWidget(self.report_page)
        if user.role == "admin":
            self.user_page = RoleManagerPage()
            self.stack.addWidget(self.user_page)

        # При изменении товаров обновляем операции
        self.product_page.data_changed.connect(self.operation_page.reload)

        # — Верхний тулбар
        top_bar = QtWidgets.QWidget()
        hl = QtWidgets.QHBoxLayout(top_bar)
        hl.setContentsMargins(8, 8, 8, 8)
        hl.setSpacing(12)

        btn_switch = QtWidgets.QPushButton("🔄")
        btn_switch.setFixedSize(32, 32)
        btn_switch.clicked.connect(self.on_switch_account)

        lbl_title = QtWidgets.QLabel("ERP-Интерфейс: Учёт продукции")
        lbl_title.setAlignment(QtCore.Qt.AlignCenter)

        btn_theme = QtWidgets.QPushButton()
        btn_theme.setFixedSize(32, 32)
        lbl_theme = QtWidgets.QLabel()
        btn_theme.clicked.connect(
            lambda: toggle_theme(btn_theme, lbl_theme, lbl_title, btn_switch, None)
        )

        hl.addWidget(btn_switch)
        hl.addStretch()
        hl.addWidget(lbl_title, stretch=1)
        hl.addStretch()
        hl.addWidget(lbl_theme)
        hl.addWidget(btn_theme)
        update_theme_ui(btn_theme, lbl_theme, lbl_title, btn_switch, None)

        # — Компоновка центральной части
        central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(top_bar)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.nav_list)
        splitter.addWidget(self.stack)
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter)

        self.setCentralWidget(central)

        # Стартовая страница
        self.nav_list.setCurrentRow(0)
        logger.info("MainWindow initialized for user '%s'", user.username)

    def on_nav_changed(self, index):
        self.stack.setCurrentIndex(index)

    def on_switch_account(self):
        self.hide()
        dlg = self.make_login_dialog()
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            new_user = dlg.user
            logger.info("Switching account: now user '%s'", new_user.username)
            new_win = MainWindow(new_user, self.make_login_dialog)
            new_win.show()
        else:
            self.show()