# gui/role_manager.py
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QSizePolicy
from services.user_service import UserService
from gui.registration_dialog import RegistrationDialog
import logging

logger = logging.getLogger(__name__)

class RoleManagerPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(8, 8, 8, 8)
        v.setSpacing(6)

        tb = QtWidgets.QHBoxLayout()
        self.btn_add = QtWidgets.QPushButton("Добавить пользователя")
        self.btn_del = QtWidgets.QPushButton("Удалить пользователя")
        tb.addWidget(self.btn_add)
        tb.addWidget(self.btn_del)
        tb.addStretch()
        v.addLayout(tb)

        self.table = QtWidgets.QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Логин", "Роль"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        v.addWidget(self.table, stretch=1)

        self.btn_add.clicked.connect(self.add_user)
        self.btn_del.clicked.connect(self.delete_user)

        self.reload()

    def reload(self):
        try:
            users = UserService.list_all()
        except Exception as e:
            logger.error("Ошибка загрузки пользователей: %s", e, exc_info=True)
            users = []
        self.table.setRowCount(0)
        for u in users:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QtWidgets.QTableWidgetItem(str(u.id)))
            self.table.setItem(r, 1, QtWidgets.QTableWidgetItem(u.username))
            self.table.setItem(r, 2, QtWidgets.QTableWidgetItem(u.role))

    def add_user(self):
        dlg = RegistrationDialog()
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            # dlg.user уже создан сервисом UserService
            logger.info("User '%s' created via GUI", dlg.user.username)
            self.reload()

    def delete_user(self):
        row = self.table.currentRow()
        if row < 0:
            return
        user_id = int(self.table.item(row, 0).text())
        if user_id == 1:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Нельзя удалить администратора")
            return
        reply = QtWidgets.QMessageBox.question(
            self, "Подтвердить", "Вы уверены, что хотите удалить пользователя?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply != QtWidgets.QMessageBox.Yes:
            return
        try:
            UserService.delete(user_id)
            self.reload()
        except Exception as e:
            logger.error("Не удалось удалить пользователя: %s", e, exc_info=True)
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Не удалось удалить пользователя")
