from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    code = Column(String(255), primary_key=True, index=True)
    gender = Column(String(5))
    age = Column(Integer)
    
    #images = relationship("Image", back_populates="user")