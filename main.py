from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status, Depends
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

import logging
import uuid
import os

from Service.User.UserService import UserService
from Service.Image.ImageService import ImageService
from model.Requests.User import UserRequest

user_service = UserService()
image_service = ImageService(os.path.join(os.path.dirname(__file__), "static"))

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s \n%(levelname)s: \t %(message)s"
)

app = FastAPI(root_path="/api/v1", docs_url="/api/docs")

app.mount("/static", StaticFiles(directory="static"), name="static")

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
async def upload_image(image: UploadFile = File(...), code: str = Form(...)):
    new_image_name = f"{code}.{image.filename.split(".")[-1]}"
    image_location = os.path.join(os.path.dirname(__file__), "static", "Img", new_image_name)
    
    with open(image_location, "wb") as f:
        f.write(await image.read())
        
    result = image_service.create_image(code, new_image_name)
    
    logging.info(result)
    return result


@app.get("/test", tags=["tmp_test"])
async def test_page(code: str):
    return user_service.read_by_code(code)
