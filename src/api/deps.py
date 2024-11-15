from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
import jwt
from pydantic import ValidationError


from src.core import config


security_scheme = HTTPBearer()


async def authenticate_request(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> str: # type: ignore
    try:
        token = credentials.credentials
        decoded_jwt_token = jwt.decode(
            token, config.KEY, algorithms=[config.ALGORITHM]
        )
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return decoded_jwt_token
