from datetime import datetime, timedelta
from typing import Any, Union
from passlib.context import CryptContext

import jwt

from src.core import config

pwd_context = CryptContext(schemes=[config.CRYPT_CONTEXT_SCHEME])


def create_access_token(data: Union[str, Any], expire_time) -> str:
    if expire_time:
        expire = datetime.utcnow() + expire_time
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=int(60 * 24 * 8)
        )
    to_encode = {"exp": expire, "sub": str(data)}
    encoded_jwt = jwt.encode(payload=to_encode, key=config.KEY, algorithm=config.ALGORITHM)
    return encoded_jwt
