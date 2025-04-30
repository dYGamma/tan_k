# gui/dashboard_window.py

from PyQt5 import QtWidgets, QtCore, QtGui
from utils.theme_manager import toggle_theme, update_theme_ui, init_theme
from gui.product_manager import ProductManagerPage
from gui.supply_history import OperationPage
from gui.report_generator import ReportPage
from gui.supplier_manager import SupplierManagerPage
from gui.warehouse_manager import WarehouseManagerPage
from gui.role_manager import RoleManagerPage
import logging

logger = logging.getLogger(__name__)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, user, make_login_dialog):
        super().__init__()
        self.user = user
        self.make_login_dialog = make_login_dialog

        # Инициализируем тему (например, dark_teal по умолчанию)
        init_theme('dark_teal')

        # Настраиваем окно
        self.setWindowTitle(f"Inventory System — {user.role}")
        self.resize(1024, 768)

        # --- Навигационная панель слева ---
        self.nav_list = QtWidgets.QListWidget()
        self.nav_list.setFixedWidth(180)
        self.nav_list.addItem("📦 Товары")
        self.nav_list.addItem("🔄 Операции")
        self.nav_list.addItem("📊 Отчёты")
        self.nav_list.addItem("🏬 Склады")
        self.nav_list.addItem("🚚 Поставщики")
        if user.role == "admin":
            self.nav_list.addItem("👥 Пользователи")
        self.nav_list.currentRowChanged.connect(self.on_nav_changed)

        # --- Стек страниц справа ---
        self.product_page   = ProductManagerPage()
        self.operation_page = OperationPage()
        self.report_page    = ReportPage()
        self.warehouse_page = WarehouseManagerPage()
        self.supplier_page  = SupplierManagerPage()

        self.stack = QtWidgets.QStackedWidget()
        self.stack.addWidget(self.product_page)
        self.stack.addWidget(self.operation_page)
        self.stack.addWidget(self.report_page)
        self.stack.addWidget(self.warehouse_page)
        self.stack.addWidget(self.supplier_page)
        if user.role == "admin":
            self.user_page = RoleManagerPage()
            self.stack.addWidget(self.user_page)

        # Сигналы перезагрузки/обновления между страницами
        self.product_page.data_changed.connect(self.operation_page.reload)
        self.operation_page.reload_request.connect(self.product_page.reload)
        self.warehouse_page.data_changed.connect(self.operation_page.reload)

        # --- Верхний тулбар ---
        top_bar = QtWidgets.QWidget()
        hl = QtWidgets.QHBoxLayout(top_bar)
        # Небольшие отступы, чтобы контент чуть отошёл от краёв
        hl.setContentsMargins(8, 8, 8, 4)
        hl.setSpacing(4)

        # Центрированный заголовок
        lbl_title = QtWidgets.QLabel("ERP-Интерфейс: Учёт продукции")
        lbl_title.setAlignment(QtCore.Qt.AlignCenter)

        # Кнопка смены аккаунта (иконка выхода)
        btn_switch = QtWidgets.QPushButton()
        btn_switch.setFixedSize(32, 32)
        btn_switch.setIconSize(QtCore.QSize(20, 20))
        btn_switch.clicked.connect(self.on_switch_account)

        # Кнопка переключения темы (иконка солнце/луна)
        btn_theme = QtWidgets.QPushButton()
        btn_theme.setFixedSize(32, 32)
        btn_theme.setIconSize(QtCore.QSize(20, 20))
        btn_theme.clicked.connect(lambda: toggle_theme(btn_theme, lbl_title, btn_switch))

        # Инициализируем иконки и стили сразу
        update_theme_ui(btn_theme, lbl_title, btn_switch)

        # Собираем HBox: отступ, заголовок, отступ, правая группа
        hl.addStretch()
        hl.addWidget(lbl_title, stretch=1)
        hl.addStretch()

        # Правая вертикальная группа для кнопок
        right_vbox = QtWidgets.QVBoxLayout()
        # Небольшие внутренние отступы
        right_vbox.setContentsMargins(0, 0, 0, 0)
        # Небольшой gap между кнопками
        right_vbox.setSpacing(4)
        # Прижимаем кнопки к верхнему краю
        right_vbox.addWidget(btn_switch, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        right_vbox.addWidget(btn_theme,  alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        right_vbox.addStretch()

        # Оборачиваем VBox в виджет, чтобы корректно сработало выравнивание
        right_container = QtWidgets.QWidget()
        right_container.setLayout(right_vbox)
        hl.addWidget(right_container, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        # --- Центральная часть: toolbar + splitter с навигацией и страницами ---
        central = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout(central)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        vbox.addWidget(top_bar)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.nav_list)
        splitter.addWidget(self.stack)
        splitter.setStretchFactor(1, 1)
        vbox.addWidget(splitter)

        self.setCentralWidget(central)

        # Устанавливаем первую вкладку
        self.nav_list.setCurrentRow(0)
        logger.info("MainWindow initialized for user '%s'", user.username)

    def on_nav_changed(self, index: int):
        """Меняем страницу в стекере при клике в списке."""
        self.stack.setCurrentIndex(index)

    def on_switch_account(self):
        """Диалог смены аккаунта."""
        self.hide()
        dlg = self.make_login_dialog()
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            new_user = dlg.user
            logger.info("Switching account: now user '%s'", new_user.username)
            new_win = MainWindow(new_user, self.make_login_dialog)
            new_win.show()
        else:
            self.show()
