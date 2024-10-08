from model.User import User
from ..SessionManager import SessionManager

class UserService:
    def create_user(self, user_request:):
        
    def read_all(self):
        with SessionManager() as db:
            users = db.query(User).all()
            return users