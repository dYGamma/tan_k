import sys
import os
import logging.config
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings
from database import initialize_db, engine
from utils.config_loader import get_config_path, load_config
from utils.logger import setup_logging
from services.session_manager import session_scope
from gui.login_window import LoginWindow

from gui.dashboard_window import MainWindow
from utils.theme_manager import init_theme, apply_input_styles

def main():
    # 1) Загрузка конфига
    cfg_path = get_config_path()
    cfg = load_config(cfg_path)

    # 2) Создаём папку для логов
    os.makedirs('logs', exist_ok=True)

    # 3) Настройка логирования
    log_cfg = os.path.join(os.path.dirname(__file__), 'log_config.ini')
    setup_logging(log_cfg)

    logging.getLogger(__name__).info("Application start")

    # 4) Инициализация БД
    initialize_db()

    # 5) Qt-приложение и тема
    app = QApplication(sys.argv)

    # Восстанавливаем тему из QSettings
    settings = QSettings('MyCompany', 'InventoryApp')
    last_theme = settings.value('theme', cfg['app']['theme'])
    init_theme(last_theme)
    apply_input_styles()

    # 6) Запуск диалога логина
    login = LoginWindow()
    if login.exec_() != LoginWindow.Accepted:
        sys.exit(0)
    user = login.user

    # 7) Главное окно
    window = MainWindow(user, make_login_dialog=LoginWindow)
    window.show()

    ret = app.exec_()
    # Сохраняем тему
    from utils.theme_manager import current_theme
    settings.setValue('theme', current_theme)
    logging.getLogger(__name__).info("Application end")
    sys.exit(ret)

if __name__ == '__main__':
    main()
