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
    NAV_WIDTH = 150  # ширина панели навигации в пикселях

    def __init__(self, user, make_login_dialog):
        super().__init__()
        self.user = user
        self.make_login_dialog = make_login_dialog

        init_theme('dark_teal')

        self.setWindowTitle(f"Inventory System — {user.role}")
        self.resize(1524, 768)

        # Навигационная панель
        self.nav_list = QtWidgets.QListWidget()
        self.nav_list.setFixedWidth(self.NAV_WIDTH)
        self.nav_list.addItems([
            "📦 Товары",
            "🔄 Операции",
            "📊 Отчёты",
            "🏬 Склады",
            "🚚 Поставщики"
        ])
        if user.role == "admin":
            self.nav_list.addItem("👥 Пользователи")
        self.nav_list.currentRowChanged.connect(self.on_nav_changed)

        # Страницы
        self.product_page   = ProductManagerPage()
        self.operation_page = OperationPage()
        self.report_page    = ReportPage()
        self.warehouse_page = WarehouseManagerPage()
        self.supplier_page  = SupplierManagerPage()

        self.stack = QtWidgets.QStackedWidget()
        for w in (self.product_page, self.operation_page, self.report_page,
                  self.warehouse_page, self.supplier_page):
            self.stack.addWidget(w)
        if user.role == "admin":
            self.user_page = RoleManagerPage()
            self.stack.addWidget(self.user_page)

        # Сигналы
        self.product_page.data_changed.connect(self.operation_page.reload)
        self.operation_page.reload_request.connect(self.product_page.reload)
        self.warehouse_page.data_changed.connect(self.operation_page.reload)

        # Верхний тулбар
        top_bar = QtWidgets.QWidget()
        top_bar.setFixedHeight(80)
        hl = QtWidgets.QHBoxLayout(top_bar)
        hl.setContentsMargins(4, 4, 4, 2)
        hl.setSpacing(2)

        # Общая информация
        self.lbl_info = QtWidgets.QLabel()
        font = self.lbl_info.font()
        font.setPointSize(10)
        self.lbl_info.setFont(font)
        self.lbl_info.setAlignment(QtCore.Qt.AlignCenter)
        self.update_dashboard_info()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_dashboard_info)
        self.timer.start(1000)

        # Кнопки справа
        btn_switch = QtWidgets.QPushButton()
        btn_switch.setFixedSize(35, 35)
        btn_switch.setIconSize(QtCore.QSize(16, 16))
        btn_switch.clicked.connect(self.on_switch_account)

        btn_theme = QtWidgets.QPushButton()
        btn_theme.setFixedSize(35, 35)
        btn_theme.setIconSize(QtCore.QSize(16, 16))
        btn_theme.clicked.connect(lambda: toggle_theme(btn_theme, self.lbl_info, btn_switch))
        update_theme_ui(btn_theme, self.lbl_info, btn_switch)

        hl.addStretch()
        hl.addWidget(self.lbl_info, stretch=1)
        hl.addStretch()

        right_vbox = QtWidgets.QVBoxLayout()
        right_vbox.setContentsMargins(0, 0, 0, 0)
        right_vbox.setSpacing(2)
        right_vbox.addWidget(btn_switch, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        right_vbox.addWidget(btn_theme,  alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        right_vbox.addStretch()

        right_container = QtWidgets.QWidget()
        right_container.setLayout(right_vbox)
        hl.addWidget(right_container, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        # Собираем окно
        central = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout(central)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        vbox.addWidget(top_bar)

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.addWidget(self.nav_list)
        self.splitter.addWidget(self.stack)
        self.splitter.setStretchFactor(1, 1)
        vbox.addWidget(self.splitter)

        self.setCentralWidget(central)
        self.nav_list.setCurrentRow(0)

        # После того, как все размеры будут рассчитаны, подгоняем сплиттер
        QtCore.QTimer.singleShot(0, self._adjust_splitter)

        logger.info("MainWindow initialized for user '%s'", user.username)

    def _adjust_splitter(self):
        """Устанавливает начальное положение ручки сплиттера."""
        total_width = self.splitter.size().width()
        self.splitter.setSizes([self.NAV_WIDTH, total_width - self.NAV_WIDTH])

    def update_dashboard_info(self):
        current_time = QtCore.QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        total_products   = self.product_page.get_total_count()
        total_operations = self.operation_page.get_total_count()
        total_suppliers  = self.supplier_page.get_total_count()
        total_warehouses = self.warehouse_page.get_total_count()
        info_text = (
            f"Добро пожаловать: {self.user.username} | "
            f"Роль: {self.user.role} | "
            f"Время: {current_time} | "
            f"Товары: {total_products} | "
            f"Операции: {total_operations} | "
            f"Поставщики: {total_suppliers} | "
            f"Склады: {total_warehouses}"
        )
        self.lbl_info.setText(info_text)

    def on_nav_changed(self, index: int):
        self.splitter.widget(1).setCurrentIndex(index)

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
