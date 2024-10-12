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
from Service.Email.MailService import MailService

from model.Requests.User import UserRequest
from model.Requests.Mail import MailRequest

root_path = os.path.dirname(__file__)

user_service = UserService()
image_service = ImageService(os.path.join(root_path, "static"))
mail_service = MailService(root_path)

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
    image_location = os.path.join(
        os.path.dirname(__file__), "static", "Img", new_image_name
    )

    with open(image_location, "wb") as f:
        f.write(await image.read())

    result = image_service.create_image(code, new_image_name)

    logging.info(result)
    return result


@app.post("/send/mail", tags=["mail"])
async def send_mail(mail_request:MailRequest):
    body_html = mail_service.create_body(code=mail_request.code)
    msg = mail_service.send_mail(to_email=mail_request.email, code=mail_request.code, body_html=body_html)
    return {"msg": msg}


@app.get("/test", tags=["tmp_test"])
async def test_page(code: str):
    return user_service.read_by_code(code)
