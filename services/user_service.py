import logging
from models.user import User
from services.session_manager import session_scope

logger = logging.getLogger(__name__)

class UserService:

    @staticmethod
    def authenticate(username: str, password: str):
        with session_scope() as s:
            user = s.query(User).filter_by(username=username).first()
            if user and user.check_password(password):
                logger.info("User '%s' authenticated", username)
                return user
        return None

    @staticmethod
    def create(username: str, raw_password: str, role: str):
        from utils.data_validator import validate_username, validate_password
        if not validate_username(username):
            raise ValueError("Invalid username")
        if not validate_password(raw_password):
            raise ValueError("Password too short")
        with session_scope() as s:
            u = User(username=username, role=role)
            u.set_password(raw_password)
            s.add(u)
            logger.info("User '%s' created", username)
            return u

    @staticmethod
    def delete(user_id: int):
        with session_scope() as s:
            u = s.get(User, user_id)
            if u:
                s.delete(u)
                logger.warning("User id=%d deleted", user_id)
                return True
        return False

    @staticmethod
    def list_all():
        with session_scope() as s:
            return s.query(User).order_by(User.username).all()
