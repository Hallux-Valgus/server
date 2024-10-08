from fastapi import FastAPI, UploadFile, HTTPException, status, Depends
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

import uuid

from database import engine, get_db
from Service.UserService import UserService

user_service = UserService()

app = FastAPI(root_path="/api/v1", docs_url="/api/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginData(BaseModel):
    username: str
    password: str


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
async def create_user_info(request, db: Session = Depends(get_db)):
    pass


@app.get("/test", tags=["tmp_test"])
async def test_page():
    return user_service.read_all()