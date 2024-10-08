from fastapi import FastAPI, UploadFile, HTTPException, status, Depends
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

import uuid

from model.User import User as user
from model.models import Base, User
from database import engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(root_path="/api/v1", docs_url="/api/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginData(BaseModel):
    username:str
    password:str

@app.post("/login", tags=["auth"])
async def test_login_response(data: LoginData):
    if data.username == "test" and data.password == "1234":
        return {"message": "Login Success"}
    else:
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    
@app.get("/get/code", tags=["user_info"])
async def create_code():
    return uuid.uuid4()

@app.post("/create/user", tags=["user_info"])
async def create_user_info(request: user, db:Session = Depends(get_db)):
    # db_user = db.query(User).filter(User.code == user.code).first()
    
    # if db_user:
    #     raise HTTPException(status_code=400, detail="code was already registered")

    new_user = User(code = user.code, gender = user.gender, age = user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user