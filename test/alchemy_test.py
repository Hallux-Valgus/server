from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine(
    "mysql+pymysql://jorim:1234@localhost:3306/test", echo=True
)

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    code = Column(String(255), primary_key=True, index=True)
    gender = Column(String(5))
    age = Column(Integer)
    
SessionLocal = sessionmaker(autoflush=False, bind=engine)

def create_user(code: str, age:int, gender: str):
    db: Session = SessionLocal()
    new_user = User(code=code, age=age, gender=gender)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # 새로 추가한 객체를 업데이트
    db.close()
    return new_user

def read_user(code:str):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.code == code).first()
    db.close()
    return user

def update_user(code:str, age:int):
    db: Session=SessionLocal()
    user = db.query(User).filter(User.code == code).first()
    if user:
        user.code = code
        user.age = age
        db.commit()
        db.refresh(user)
    db.close()
    return user

def delete_user(code:str):
    db:Session = SessionLocal()
    user = db.query(User).filter(User.code == code).first()
    if user:
        db.delete(user)
        db.commit()
    db.close()
    return "delete fin"

#print(create_user("12345", "남성", 10))
print(read_user("test_code"))
print(update_user("test_code", 10))
#print(delete_user("test_code"))