from pydantic import BaseModel
class UserRequest(BaseModel):
    code:str
    gender:str
    age:int