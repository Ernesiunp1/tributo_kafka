"""Routes for /admin/*"""
import copy
from typing import Dict, List, Optional
from fastapi import APIRouter
from fastapi import Depends, HTTPException

import app.anfler.api.api_schemas as api_schemas
import anfler.db.schemas as db_schemas
import anfler.util.log.lw as lw
import anfler.util.msg.message as msg
import anfler.util.jwt.jwt_helper as jwtw

from app.anfler.api import deps
from app.anfler.api import api_security
from anfler.db.database import DBWrapper, message_to_job_request
from anfler.kafka_wrapper.kw import KafkaProducerWrapper
from anfler.util.helper import dpath

_log= lw.get_logger("anfler.api.admin")

router = APIRouter(tags=["admin"])

# ---------------------------------------------------------------------------
#   Route
# ---------------------------------------------------------------------------
@router.get("/admin/services", response_model=List[api_schemas.JobServices])
async def get_services(db: DBWrapper = Depends(deps.get_db),
                           token_data = Depends(api_security.get_token_data)):
    """List of defined services"""
    try:
        services= db.get_services()
    except Exception as e:
        _log.error(f"Getting error accessing DB: {e.message}")
        raise HTTPException(status_code=500, detail=f"Getting error accessing DB: {e.message}")
    return [api_schemas.JobServices(id=service.id,
                                    fn=service.fn,
                                    service=service.service,
                                    entity=service.entity) for service in services]
#
# @router.get("/admin/services/{entity}",response_model=List[api_schemas.JobServices])
# async def get_services(entity:db_schemas.Entities,
#                        db:DBWrapper=Depends(deps.get_db), username: str = Depends(api_security.get_current_username)):

@router.get("/admin/services/{entity}", response_model=List[api_schemas.JobServices])
async def get_services(entity: db_schemas.Entities,
                           db: DBWrapper = Depends(deps.get_db),
                           token_data=Depends(api_security.get_token_data)):
    """List of defined services by entity"""
    services= db.get_services(entity.value)
    return [api_schemas.JobServices(id=service.id,
                                    fn=service.fn,
                                    service=service.service,
                                    entity=service.entity) for service in services]


@router.post("/admin/token", response_model=api_schemas.Token)
async def get_token(payload:Dict, username: str = Depends(api_security.get_current_username)):
    """Get a JWT token
    """
    return api_security.response(jwtw.jwt_encode({"username":username}))