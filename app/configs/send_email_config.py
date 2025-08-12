import os
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

SMTP_PORT = int(os.getenv("SMTP_PORT"))
VERIFY_URL_BASE = os.getenv("VERIFY_URL_BASE")
NEW_TOKEN_URL_BASE = os.getenv("NEW_TOKEN_URL_BASE")