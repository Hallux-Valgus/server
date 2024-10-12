from pydantic import BaseModel

class MailRequest(BaseModel):
    email: str
    code: str