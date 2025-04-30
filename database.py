import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from utils.config_loader import load_config, get_config_path
import logging

# Загрузка конфига для БД
cfg = load_config(get_config_path())
db_url = cfg['database']['url']

# Создание папки под SQLite, если нужно
if db_url.startswith('sqlite:///'):
    path = db_url.replace('sqlite:///', '')
    os.makedirs(os.path.dirname(path), exist_ok=True)

engine = create_engine(db_url, echo=False, future=True)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,  # <--- добавьте эту строку
)
Base = declarative_base()

def initialize_db():
    from models.user import User
    from models.product import Product
    from models.supplier import Supplier
    from models.operation import Operation
    Base.metadata.create_all(bind=engine)

    # Default admin
    from services.user_service import UserService
    import sqlalchemy.exc
    try:
        with SessionLocal() as s:
            u = s.query(User).filter_by(username='admin').first()
            if not u:
                admin = User(username='admin', role='admin')
                admin.set_password('admin')
                s.add(admin)
                s.commit()
                logging.getLogger(__name__).info("Default admin created")
    except sqlalchemy.exc.SQLAlchemyError as e:
        logging.getLogger(__name__).error("Error creating default admin: %s", e, exc_info=True)
