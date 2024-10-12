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

    def create_body(self, code:str):
        html = f"""
        <html>
        <body>
            <h1>code: {code}</h1>
            <p>아래를 보세요</p>
            <img src='cid:image1'/>
        </body>
        </html>
        """
        
        return html

    def send_mail(self, to_email:str, code:str, body_html:str):
        msg = MIMEMultipart()
        msg["From"] = self.smtp_user
        msg["To"] = to_email
        msg["Subject"] = "[HFoot] 결과 이미지입니다"
        
        #msg.attach(MIMEText("Just Testing", "plain"))
        
        msg.attach(MIMEText(body_html, 'html'))
        
        image_path = os.path.join(self.root_path, "static", "Img", "/Users/janghyolim/Desktop/code/HFoot/static/Img/f3cf6e7e-dbf8-4d56-86f7-59bcdc8b7532.jpg")
        
        with open(image_path, "rb") as f:
            mime_image = MIMEImage(f.read())
            #mime_image.add_header("Content-Disposition", f"attachment; filename={Path(image_path).name}")
            mime_image.add_header("Content-ID", "<image1>")
            mime_image.add_header("Content-Disposition", "inline", filename=Path(image_path).name)
            msg.attach(mime_image)
        
        try:
            server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            # server.starttls()
            server.login(self.smtp_user, self.smtp_pass)
            server.send_message(msg)
            server.quit()
            return "success"
        except Exception as e:
            return f"fail with error: {e}"