from fastapi import FastAPI, UploadFile, HTTPException, status
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from model.User import User

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
    
@app.post("/create/code", tags=["info"])
async def create_code(request: User):
    return User