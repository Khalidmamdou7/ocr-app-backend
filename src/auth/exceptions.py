# exceptions.py
# This is the exceptions module.
# module specific exceptions, e.g. PostNotFound, ItemAlreadyExists, etc. go here

from fastapi import HTTPException, status

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

INCORRECT_USERNAME_PASSWORD_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username/email/mobile or password",
    headers={"WWW-Authenticate": "Bearer"},
)
