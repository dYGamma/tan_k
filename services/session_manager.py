# services/session_manager.py

from contextlib import contextmanager
from database import SessionLocal

@contextmanager
def session_scope():
    """
    Контекстный менеджер для SQLAlchemy-сессии.
    Открывает сессию, кидает commit при нормальном завершении,
     rollback при ошибке и всегда закрывает сессию.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
