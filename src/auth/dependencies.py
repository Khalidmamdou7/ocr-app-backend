# router dependencies
# This is the dependencies module. https://fastapi.tiangolo.com/tutorial/dependencies/



from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from .utils import decode_access_token
from .exceptions import CREDENTIALS_EXCEPTION
from .models import UserInDB
from .schemas import UsersDB


jwt_scheme = HTTPBearer()


async def authenticate_user_jwt(
    token: HTTPAuthorizationCredentials = Depends(jwt_scheme),
):
    try:
        payload = decode_access_token(token.credentials)
        username = payload.get("username")
        user = UsersDB().get_user(username)
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    
async def get_current_user(user: UserInDB = Depends(authenticate_user_jwt)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This account has not been verified yet, please check your email to confirm your account",
        )
    return user
