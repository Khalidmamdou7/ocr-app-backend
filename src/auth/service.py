# service.py
# Module specific business logic goes here

from typing import Annotated
from datetime import timedelta
from ..utils.mailer import Mailer
from pydantic import EmailStr

from ..config import APP_SETTINGS


from fastapi import Depends, HTTPException, status

from .models import *
from .schemas import UsersDB
from .utils import (
    verify_password,
    create_access_token,
    decode_access_token,
    get_password_hash,
)
from .exceptions import CREDENTIALS_EXCEPTION, INCORRECT_USERNAME_PASSWORD_EXCEPTION


async def create_user(user: UserCreateRequest) -> UserCreateResponse:
    user_in_db = user.model_dump()
    user_in_db["hashed_password"] = get_password_hash(user.password)


    new_user = UsersDB().add_user(UserInDB(**user_in_db))
    # TODO: Change this to send email asynchronously (background task)
    await send_confirmation_email(user)

    return new_user


def login(identifier: str, password: str):
    # TODO: Update this function to be resistant to timing attacks

    user = UsersDB().get_user(identifier)
    if not verify_password(password, user.hashed_password):
        raise INCORRECT_USERNAME_PASSWORD_EXCEPTION
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This account has not been verified yet, please check your email to confirm your account",
        )

    access_token_expires = timedelta(minutes=APP_SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=user.model_dump(),
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


def confirm_email(email: str, token: str):
    user = UsersDB().get_user(email)    
    if not decode_access_token(token).get("username") == user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    user.disabled = False
    UsersDB().update_user(user)


async def resend_confirmation_email(email: EmailStr):
    user = UsersDB().get_user(email)
    if not user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This account has already been verified",
        )
    await send_confirmation_email(user)


async def send_confirmation_email(user: User):
    print("Sending confirmation email")
    mailer = Mailer()
    confirmation_token = create_access_token(data=user.model_dump())
    confirmation_link = f"{APP_SETTINGS.APP_DOMAIN}/auth/confirm/{confirmation_token}?email={user.email}"
    mailer.send_confirmation_email(user.email, confirmation_link)


def forgot_password(email: EmailStr):
    user = UsersDB().get_user(email)
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This account has not been verified yet, please confirm your account first",
        )
    mailer = Mailer()
    reset_token = create_access_token(data=user.model_dump())

    reset_link = (
        f"{APP_SETTINGS.CLIENT_DOMAIN}/reset-password/{reset_token}?email={user.email}"
    )
    mailer.send_reset_password_email(user.email, reset_link)


def reset_password(email: EmailStr, token: str, new_password: str):
    user = UsersDB().get_user(email)
    if not decode_access_token(token).get("username") == user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    user.hashed_password = get_password_hash(new_password)
    UsersDB().update_user(user)
    Mailer().send_notification_email(
        user.email, "Your password has been reset successfully"
    )


def create_admin_user():
    # TODO: The flow of this function could be improved (eliminate the need for the if else block)


    print("Trying to create admin user")
    admin_user = UserInDB(
        full_name="Admin",
        username=APP_SETTINGS.ADMIN_USERNAME,
        email=APP_SETTINGS.ADMIN_EMAIL,
        mobile=APP_SETTINGS.ADMIN_MOBILE,
        hashed_password=get_password_hash(APP_SETTINGS.ADMIN_PASSWORD.get_secret_value()),
        role=RoleEnum.ADMIN,
        disabled=False,
    )
    isAdminUserCreated = UsersDB().get_admin_user()
    if isAdminUserCreated:        
        print("Admin user already exists")
    else:
        UsersDB().add_user(admin_user)
        print("Admin user created successfully")

def assign_role(user_identifier: str, role: RoleEnum):
    if role == RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't assign the admin role to a user",
        )

    user = UsersDB().get_user(user_identifier)
    if user.role == RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't change the role of the admin user",
        )
    
    print("Assigning role: ", role)
    print("To user: ", user)
    user.role = role
    UsersDB().update_user(user)
    Mailer().send_notification_email(
        user.email, f"Your role has been updated to a/an {role.value}"
    )
    return user

