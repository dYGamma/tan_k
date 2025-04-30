from sqlalchemy import Column, Integer, String
from database import Base
from utils.password_utils import hash_password, verify_password
import logging

logger = logging.getLogger(__name__)

class User(Base):
    __tablename__ = "users"

    id       = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role     = Column(String, nullable=False)

    def set_password(self, raw_password: str):
        self.password = hash_password(raw_password)
        logger.info("Password set for user '%s'", self.username)

    def check_password(self, raw_password: str) -> bool:
        ok = verify_password(raw_password, self.password)
        if not ok:
            logger.warning("Failed login attempt for '%s'", self.username)
        return ok
