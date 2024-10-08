from model.User import User
from ..SessionManager import SessionManager

from model.Requests.User import UserRequest
from model.User import User

class UserService:
    def create_user(self, request:UserRequest):
        with SessionManager() as db:
            new_user = User(code = request.code, gender = request.gender, age = request.age)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            db.close()
        return new_user
            
        
    def read_all(self):
        with SessionManager() as db:
            users = db.query(User).all()
            return users
        
    def read_by_code(self, code:str):
        with SessionManager() as db:
            user = db.query(User).filter(User.code == code).first()
            db.close()
            return user