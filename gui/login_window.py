# gui/login_window.py
from PyQt5 import QtWidgets, QtCore
from services.user_service import UserService
import logging

logger = logging.getLogger(__name__)

class LoginWindow(QtWidgets.QDialog):
    login_success = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход")
        self.setFixedSize(350, 200)
        layout = QtWidgets.QVBoxLayout(self)

        # Поля ввода
        self.username = QtWidgets.QLineEdit()
        self.username.setPlaceholderText("Логин")
        self.password = QtWidgets.QLineEdit()
        self.password.setPlaceholderText("Пароль")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        # Кнопки Войти / Регистрация
        hl = QtWidgets.QHBoxLayout()
        btn_login = QtWidgets.QPushButton("Войти")
        btn_login.clicked.connect(self.on_login)
        btn_reg = QtWidgets.QPushButton("Регистрация")
        btn_reg.clicked.connect(self.on_register)
        hl.addWidget(btn_login)
        hl.addWidget(btn_reg)

        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addLayout(hl)

        self.user = None

    def on_login(self):
        username = self.username.text().strip()
        password = self.password.text()
        try:
            user = UserService.authenticate(username, password)
        except Exception as e:
            logger.error("Ошибка при аутентификации: %s", e, exc_info=True)
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Внутренняя ошибка при входе")
            return

        if user:
            self.user = user
            logger.info("User '%s' logged in via GUI", username)
            self.login_success.emit(user)
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверные учётные данные")

    def on_register(self):
        from gui.registration_dialog import RegistrationDialog
        dlg = RegistrationDialog()
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            # После успешной регистрации можно автозалогинить или предложить войти
            QtWidgets.QMessageBox.information(self, "Успех", "Теперь войдите в систему")
