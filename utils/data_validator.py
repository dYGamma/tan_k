# utils/data_validator.py
import re

def validate_username(username: str) -> bool:
    return bool(re.match(r"^[A-Za-z0-9_]{3,20}$", username))

def validate_password(password: str) -> bool:
    return len(password) >= 6

def validate_nonempty(text: str) -> bool:
    return bool(text and text.strip())

def validate_positive_number(val) -> bool:
    try:
        return float(val) >= 0
    except:
        return False

def validate_product(name: str, exp: int) -> bool:
    """
    Проверяет корректность данных товара:
      - name не должна быть пустой
      - exp (срок годности в днях) неотрицательное число
    """
    return validate_nonempty(name) and validate_positive_number(exp)
