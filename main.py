from fastapi import FastAPI, UploadFile,File,Form, HTTPException, status, Depends
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

import logging
import uuid

from Service.User.UserService import UserService
from model.Requests.User import UserRequest

user_service = UserService()

logging.basicConfig(level=logging.INFO, format="%(asctime)s \n%(levelname)s: \t %(message)s")

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


@app.post("/login", tags=["admin"])
async def test_login_response(data: LoginData):
    if data.username == "test" and data.password == "1234":
        return {"message": "Login Success"}
    else:
        raise HTTPException(status_code=400, detail="Invalid Credentials")


@app.get("/get/code", tags=["user_info"])
async def create_code():
    return uuid.uuid4()


@app.get("/get/user", tags=["user_info"])
async def get_user_by_code(code: str):
    return user_service.read_by_code(code)


@app.post("/create/user", tags=["user_info"])
async def create_user_info(request: UserRequest):
    return user_service.create_user(request)


@app.post("/upload", tags=["image"])
async def upload_image(image:UploadFile = File(...), code:str=Form(...)):
    logging.info(f"{image.filename} - {code}")
    return {"image": image.filename, "code": code}


@app.get("/test", tags=["tmp_test"])
async def test_page(code: str):
    return user_service.read_by_code(code)
