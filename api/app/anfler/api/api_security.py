"""JWT Helper"""

import copy
import json
import time
from pydantic import BaseModel
from typing import Dict, Optional, List
from fastapi import (
    Depends,
    HTTPException,
    Request,
    status
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer
)

import anfler.util.log.lw as lw
import app.anfler.api.api_schemas as api_schemas
import anfler.util.jwt.jwt_helper as jwtw

# ---------------------------------------------------------------------------
#   Global objects
# ---------------------------------------------------------------------------
security_basic = HTTPBasic()

_log = lw.get_logger("anfler.api.security")


class JWTBearer(HTTPBearer):
    """Extending HTTPBeare"""
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = jwtw.jwt_decode(jwtoken)
            token_data = api_schemas.TokenData(**payload)
            # if not "username" in payload:
            #     payload={}
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

security_jwt = JWTBearer()
# ---------------------------------------------------------------------------
#   Helper functions
# ---------------------------------------------------------------------------
def response(token:str) :
    """Normalize token as Json
    :param token

    :return Dict {"access_token": <token>}
    """
    return {"access_token":token,"token_type": "bearer"}


async def get_current_username(credentials: HTTPBasicCredentials = Depends(security_basic)):
    """Dummy function to generate token
    Pending to validate username/password

    """
    correct_username = credentials.username
    correct_password = credentials.password
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


async def get_token_data(token:str=Depends(security_jwt)):
    token_data = jwtw.jwt_decode(token)
    return api_schemas.TokenData(**token_data)


