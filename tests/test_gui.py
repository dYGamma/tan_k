import pytest
from PyQt5.QtWidgets import QApplication
from gui.login_window import LoginWindow

@pytest.fixture(scope="session")
def app():
    return QApplication([])

def test_login_window_shows(app):
    w = LoginWindow()
    assert w.windowTitle() == "Вход в систему"
    w.close()
