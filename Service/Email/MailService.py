import os
# from ..SessionManager import SessionManager

from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    
    msg.attach(MIMEText("Just Testing", "plain"))
    
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