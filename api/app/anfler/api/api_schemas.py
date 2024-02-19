"""TributoSimple API schemas"""

import datetime
import uuid

from pydantic import BaseModel
from typing import List, Dict, Optional, Any

import anfler.util.constants as C
import anfler.db


class TokenData(BaseModel):
    """JWT info"""
    username: str
    exp: int
    id:Optional[int]
    iat:Optional[int]
    roles:Optional[List]

class Token(BaseModel):
    """Generated token (response)"""
    access_token: str
    token_type: str

class Me(BaseModel):
    """Response for route /me"""
    token_data:TokenData
    datetime_utc:datetime.datetime

class AuthHeaderBasic(BaseModel):
    """Basic header for messages. Required by scrap oeprations"""
    type = "basic"
    cuit:int
    password:str
    codif:int

class AuthHeader(BaseModel):
    auth = AuthHeaderBasic

class Header(BaseModel):
    """Job header"""
    auth:AuthHeaderBasic
    def mask(self):
        self.auth.password = "XXXXXX"
        return self


class Job(BaseModel):
    """Response for query routes /jobs/*"""
    id:str
    entity:str
    service:str
    user:str
    payload_in:Optional[Dict]
    payload_out: Optional[Dict]
    state:int
    status:Optional[int]
    errors: Optional[List]
    dt_created:str
    dt_updated:Optional[str]

class JobRequest(BaseModel):
    """Request for route /jobs/{entity}/{service}"""
    header: Header
    payload:Optional[Dict]

class JobResponse(BaseModel):
    """Response for route /jobs/{entity}/{service}"""
    id:str
    entity:str
    service:str
    state:int
    header: Header
    payload: Optional[Dict]
    status:Optional[int]
    errors: Optional[List]

class JobServices(BaseModel):
    """Response for route /admin/services/{entity}"""
    id:int
    fn:str
    service:str
    entity:str




