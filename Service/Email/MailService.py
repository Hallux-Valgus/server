import os
# from ..SessionManager import SessionManager

from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
from pathlib import Path

class MailService:
    root_path:str
    def __init__(self, root_path):
        self.root_path = root_path

load_dotenv()

smtp_host = os.getenv("SMTP_HOST")
smtp_port = int(os.getenv("SMTP_PORT"))
smtp_user = os.getenv("SMTP_USER")
smtp_pass = os.getenv("SMTP_PASS")

def send_mail(to_email:str):
    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = "[test] Email"
    
    #msg.attach(MIMEText("Just Testing", "plain"))
    
    html = f"""
    <html>
    <body>
        <h1>제목입니다</h1>
        <p>아래를 보세요</p>
        <img src='cid:image1'/>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(html, 'html'))
    
    image_path = "/Users/janghyolim/Desktop/code/HFoot/static/Img/063f6a23-b86a-4a82-bfbc-cc5b48023712.jpg"
    
    with open(image_path, "rb") as f:
        mime_image = MIMEImage(f.read())
        #mime_image.add_header("Content-Disposition", f"attachment; filename={Path(image_path).name}")
        mime_image.add_header("Content-ID", "<image1>")
        mime_image.add_header("Content-Disposition", "inline", filename=Path(image_path).name)
        msg.attach(mime_image)
    
    try:
        server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        # server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        print("Success to send mail")
    except Exception as e:
        print(f"Fail to send mail : {e}")


send_mail("wkdgyfla97@naver.com")