from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from model.User import User

from pydantic import BaseModel

Base = declarative_base()

class Image(Base):
    __tablename__ = "image"
    id=Column(Integer, primary_key=True, autoincrement=True)
    user_code = Column(String(255))
    image_path = Column(String(255))
    
    #user = relationship(User, primaryjoin= "user.code == image.code")
    
class ImageResponse(BaseModel):
    image_path:str
    angle:float
    
class ImageRequest(BaseModel):
    image_file:str