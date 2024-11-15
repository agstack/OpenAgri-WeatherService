from datetime import timedelta
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.api.deps import authenticate_request
from src.core import config
from src.core.security import create_access_token
from src.schemas.auth import AuthToken


logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/test")
async def get_payload(payload: dict =  Depends(authenticate_request)):
   return payload


# This is a test method to create a token and can be removed since we integrate with Gatekeeper
@auth_router.post("/token", response_model=AuthToken)
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=f"{form_data.username}:{form_data.password}", expire_time=access_token_expires
    )
    return AuthToken(jwt_token=access_token)

