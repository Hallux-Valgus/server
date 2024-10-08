from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "user"
    
    code = Column(String(255), primary_key=True, index=True)
    gender = Column(String(5), index=True)
    age = Column(Integer, index=True)