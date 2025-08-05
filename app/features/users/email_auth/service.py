from datetime import datetime, timedelta, timezone
from aiosmtplib import SMTP
import secrets
from fastapi import HTTPException, Request
from email.message import EmailMessage

from app.configs.send_email_config import SMTP_USERNAME, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT, VERIFY_URL_BASE
from app.features.users.email_auth.model import EmailAuthModel
from app.features.users.email_auth.repository import EmailAuthRepository

class EmailAuthService:
    def __init__(self, request: Request):
        self.__repository = EmailAuthRepository(request)
        
    async def create_email_model(self, email: str) -> EmailAuthModel:
        email_created = EmailAuthModel(
            email=email,
            email_verification_token=secrets.token_urlsafe(32),
            email_verification_expiry=datetime.now(timezone.utc) + timedelta(hours=48))
        await self.send_verification_email(email_created.email, email_created.email_verification_token)
        return email_created
    
    async def verify_email(self, token: str) -> None:
        user_model = await self.__repository.find_one_by_token(token)
        
        if user_model == None:
            raise HTTPException(status_code=409, detail="The email it is already verified")
        
        expiry = user_model.email_auth.email_verification_expiry
        if expiry is None or expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
            
        if expiry < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="The token is expired")
        
        await self.__repository.mark_as_verified_by_id(user_model.id)
        
    async def send_verification_email(self, to_email: str, token: str):
        msg = EmailMessage()
        msg["From"] = SMTP_USERNAME
        msg["To"] = to_email
        msg["Subject"] = "Verify your BandSync account"
        
        verification_link = f"{VERIFY_URL_BASE}?token={token}"
        
        msg.set_content(f"""Hello, thank you for registering with BandSync.
To verify your email address, click the following link:{verification_link}

This link will expire in 48 hours. If you haven't created an account, simply ignore this message.""")
        try:
            smtp = SMTP(hostname=SMTP_HOST, port=SMTP_PORT, start_tls=True)
            await smtp.connect()
            await smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
            await smtp.send_message(msg)
            await smtp.quit()
        except Exception as e:
            print(f"[ERROR] the send email failure: {e}")
            raise HTTPException(status_code=500, detail="Error sending verification email")
