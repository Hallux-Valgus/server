from pydantic import BaseModel

class User(BaseModel):
    code:str
    gender:str
    age:int
    