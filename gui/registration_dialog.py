# gui/registration_dialog.py
from PyQt5 import QtWidgets
from services.user_service import UserService
import logging

logger = logging.getLogger(__name__)

class RegistrationDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация нового пользователя")
        self.setFixedSize(400, 250)
        layout = QtWidgets.QFormLayout(self)

        self.username = QtWidgets.QLineEdit()
        self.username.setPlaceholderText("3–20 символов, латиница/цифры/_")
        self.password = QtWidgets.QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setPlaceholderText("Не менее 6 символов")
        self.role = QtWidgets.QComboBox()
        self.role.addItems(["user", "admin"])

        self.btn = QtWidgets.QPushButton("Зарегистрировать")
        self.btn.clicked.connect(self.register)

        layout.addRow("Логин", self.username)
        layout.addRow("Пароль", self.password)
        layout.addRow("Роль", self.role)
        layout.addRow(self.btn)

        self.user = None

    def register(self):
        u = self.username.text().strip()
        p = self.password.text()
        r = self.role.currentText()
        try:
            user = UserService.create(u, p, r)
            QtWidgets.QMessageBox.information(self, "Успех", "Пользователь зарегистрирован")
            self.user = user
            logger.info("New user '%s' registered via GUI", u)
            self.accept()
        except ValueError as ve:
            QtWidgets.QMessageBox.warning(self, "Ошибка", str(ve))
        except Exception as e:
            logger.error("Ошибка при регистрации: %s", e, exc_info=True)
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Не удалось зарегистрировать пользователя")
