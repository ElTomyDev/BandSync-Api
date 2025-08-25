from datetime import datetime, timedelta, timezone
from aiosmtplib import SMTP
import secrets
from fastapi import HTTPException, Request
from email.message import EmailMessage
from passlib.hash import bcrypt

from app.configs.send_email_config import SMTP_USERNAME, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT, VERIFY_URL_BASE
from app.features.users.email_auth.model import EmailAuthModel
from app.features.users.repository import UserRepository
from app.features.users.validations import UserValidations

class EmailAuthService:
    def __init__(self, request: Request):
        self.__repository = UserRepository(request)
        
    async def create_email_model(self, email: str) -> EmailAuthModel:
        UserValidations.valid_email_in_use(await self.__repository.exist_email(email), email)
        
        token = secrets.token_urlsafe(32) # Generate a token
        
        email_created = EmailAuthModel(
            email=email,
            email_verification_token_hash=bcrypt.hash(token), # save token hashed
            email_verification_expiry=datetime.now(timezone.utc) + timedelta(hours=24))
        
        await self.send_verification_email(email_created.email, token)
        
        return email_created
    
    async def verify_email(self, email: str, token: str) -> None:
        user_model = await self.__repository.find_one_by_email(email)
        UserValidations.valid_user_existence(None, user_model)
        
        UserValidations.valid_email_is_already_verify(user_model)
        
        expiry_date = user_model.email_auth.email_verification_expiry
        UserValidations.valid_email_verification_expiry(expiry_date, user_model.email_auth.email)
        
        UserValidations.valid_email_verification_token(token, user_model.email_auth.email_verification_token_hash)
        
        await self.__repository.mark_as_verified_by_id(user_model.id)
    
    async def generate_new_verify_token(self, email: str) -> None:
        token = secrets.token_urlsafe(32)
        update_result = await self.__repository.generate_new_token(bcrypt.hash(token), email)
        
        UserValidations.valid_update_or_delete_result(
            update_result.matched_count, 
            "An error occurred while trying to generate a new token"
        )
        
        await self.send_verification_email(email, token)
        
    async def send_verification_email(self, to_email: str, token: str):
        msg = EmailMessage()
        msg["From"] = SMTP_USERNAME
        msg["To"] = to_email
        msg["Subject"] = "Verify your BandSync account"
        
        verification_link = f"{VERIFY_URL_BASE}?email={to_email}&token={token}"
        
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
