# utils/theme_manager.py

from qt_material import apply_stylesheet
from PyQt5.QtWidgets import QApplication
import qtawesome as qta

# Список доступных тем и их файлы
THEMES = {
    'dark_teal': 'dark_teal.xml',
    'light_cyan_500': 'light_cyan_500.xml',
}

# Параметры для каждой темы
theme_params = {
    'dark_teal': {
        'text_color': '#cccccc',
        'input_text_color': '#cccccc',
        'input_focus_color': '#00bcd4',
        'icon_name': 'fa5s.moon',
    },
    'light_cyan_500': {
        'text_color': '#212121',
        'input_text_color': '#212121',
        'input_focus_color': '#00bcd4',
        'icon_name': 'fa5s.sun',
    },
}

current_theme = None

def init_theme(theme_name: str):
    """
    Устанавливает тему при старте приложения.
    Вызывается из MainWindow.__init__ до создания виджетов.
    """
    global current_theme
    app = QApplication.instance()
    apply_stylesheet(app, theme=THEMES[theme_name])
    current_theme = theme_name

def apply_input_styles():
    """
    Дополнительные QSS-правила для полей ввода (LineEdit, ComboBox, SpinBox и пр.).
    Применяется после смены темы.
    """
    app = QApplication.instance()
    p = theme_params[current_theme]
    qss = f"""
        /* Обычные текстовые поля и комбо-боксы */
        QLineEdit, QDateEdit, QTimeEdit, QComboBox {{
            color: {p['input_text_color']};
        }}
        QLineEdit:focus, QDateEdit:focus, QTimeEdit:focus, QComboBox:focus {{
            color: {p['input_focus_color']};
        }}
        QLineEdit::placeholder {{
            color: #888888;
        }}
        QComboBox QAbstractItemView {{
            color: {p['text_color']};
            background-color: transparent;
            selection-background-color: {p['input_focus_color']};
            selection-color: #ffffff;
        }}

        /* Поля SpinBox (для числового ввода) */
        QSpinBox, QDoubleSpinBox {{
            color: {p['input_text_color']};
        }}
        QSpinBox:focus, QDoubleSpinBox:focus {{
            color: {p['input_focus_color']};
            border: 1px solid {p['input_focus_color']};
            border-radius: 4px;
        }}
    """
    app.setStyleSheet(app.styleSheet() + qss)

def toggle_theme(theme_btn, title_lbl, switch_btn=None):
    """
    Переключает тему между светлой и тёмной,
    затем обновляет UI-элементы (иконки и стили).
    """
    global current_theme
    new = 'light_cyan_500' if current_theme == 'dark_teal' else 'dark_teal'
    app = QApplication.instance()
    apply_stylesheet(app, theme=THEMES[new])
    current_theme = new
    update_theme_ui(theme_btn, title_lbl, switch_btn)

def update_theme_ui(theme_btn, title_lbl, switch_btn=None):
    """
    Обновляет иконки и стили UI-элементов под текущую тему:
    - Кнопка темы (иконка sun/moon)
    - Заголовок окна (цвет, рамка)
    - Кнопка смены аккаунта (иконка выхода), если передана
    - Стили полей ввода
    """
    p = theme_params[current_theme]

    # Иконка кнопки темы
    theme_btn.setIcon(qta.icon(p['icon_name'], color=p['text_color']))

    # Стиль заголовка
    title_lbl.setStyleSheet(f"""
        color: {p['text_color']};
        font-size: 16px;
        font-weight: bold;
        border: 2px solid {p['text_color']};
        padding: 8px;
        border-radius: 8px;
    """)

    # Иконка кнопки смены аккаунта
    if switch_btn:
        switch_btn.setIcon(qta.icon('fa5s.sign-out-alt', color=p['text_color']))

    # Применяем стили к полям ввода
    apply_input_styles()
