from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    code = Column(String(255), primary_key=True, index=True)
    gender = Column(String(5))
    age = Column(Integer)