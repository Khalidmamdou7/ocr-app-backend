# utils.py
# Non-business logic related utility functions go here (e.g. hashing, etc.)
# Helper functions that are used in the service layer go here

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from ..config import APP_SETTINGS
from .exceptions import CREDENTIALS_EXCEPTION

from .models import TokenData

# Using bcrypt for hashing and the deprecated parameter is set to auto so that the library will automatically choose the best algorithm to use
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: TokenData, expires_delta: timedelta | None = None):
    to_encode = TokenData(**data).model_dump()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, APP_SETTINGS.SECRET_KEY.get_secret_value(), algorithm=APP_SETTINGS.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        decoded_token = jwt.decode(token, APP_SETTINGS.SECRET_KEY.get_secret_value(), algorithms=[APP_SETTINGS.ALGORITHM])
    except jwt.JWTError:
        raise CREDENTIALS_EXCEPTION
    
    return decoded_token