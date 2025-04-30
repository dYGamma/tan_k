import configparser
import os
import sys

def get_config_path():
    # Приоритет: аргумент командной строки > переменная окружения > стандартный путь
    if '--config' in sys.argv:
        idx = sys.argv.index('--config')
        return sys.argv[idx + 1]
    env = os.environ.get('INVENTORY_CONFIG')
    if env:
        return env
    return os.path.join(os.path.dirname(__file__), '..', 'config.ini')

def load_config(path: str):
    cfg = configparser.ConfigParser()
    read = cfg.read(path)
    if not read:
        raise FileNotFoundError(f"Config file not found: {path}")
    return cfg
