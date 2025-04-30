# utils/theme_manager.py

from qt_material import apply_stylesheet
from PyQt5.QtWidgets import QApplication
import qtawesome as qta

# список доступных тем
THEMES = {
    'dark_teal': 'dark_teal.xml',
    'light_cyan_500': 'light_cyan_500.xml'
}

theme_params = {
    'dark_teal': {
        'text_color': '#cccccc',
        'input_text_color': '#cccccc',
        'input_focus_color': '#00bcd4',
        'icon_name': 'fa5s.moon',
        'label_text': 'Тёмная тема',
    },
    'light_cyan_500': {
        'text_color': '#212121',
        'input_text_color': '#212121',
        'input_focus_color': '#00bcd4',
        'icon_name': 'fa5s.sun',
        'label_text': 'Светлая тема',
    },
}

current_theme = None

def init_theme(theme_name: str):
    """Устанавливает тему при старте приложения."""
    global current_theme
    app = QApplication.instance()
    apply_stylesheet(app, theme=THEMES[theme_name])
    current_theme = theme_name

def apply_input_styles():
    """Дополнительные QSS-правила для полей ввода."""
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

        /* Поля SpinBox (для "Срок(дн)" и "Количество") */
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

def toggle_theme(theme_btn, theme_lbl, title_lbl, switch_btn=None, username_lbl=None):
    """Переключает тему между светлой и тёмной."""
    global current_theme
    new = 'light_cyan_500' if current_theme == 'dark_teal' else 'dark_teal'
    app = QApplication.instance()
    apply_stylesheet(app, theme=THEMES[new])
    current_theme = new
    update_theme_ui(theme_btn, theme_lbl, title_lbl, switch_btn, username_lbl)

def update_theme_ui(theme_btn, theme_lbl, title_lbl, switch_btn=None, username_lbl=None):
    """Обновляет иконки и стили UI-элементов под текущую тему."""
    p = theme_params[current_theme]
    # Обновляем текст и цвет метки темы
    theme_lbl.setText(p['label_text'])
    theme_lbl.setStyleSheet(f"color: {p['text_color']}; font-size: 14px;")
    # Обновляем иконку кнопки темы
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
    # Иконка кнопки выхода (если есть)
    if switch_btn:
        switch_btn.setIcon(qta.icon('fa5s.sign-out-alt', color=p['text_color']))
    # Стиль имени пользователя (если есть)
    if username_lbl:
        username_lbl.setStyleSheet(f"font-size: 14px; color: {p['text_color']};")
    # Применяем дополнительные стили полей ввода
    apply_input_styles()
