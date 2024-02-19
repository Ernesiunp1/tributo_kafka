"""Routes for /jobs"""
import copy
from typing import List
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Request
)
import app.anfler.api.api_schemas as api_schemas
import anfler.db.schemas as db_schemas
import anfler.util.log.lw as lw
import anfler.util.msg.message as msg

from app.anfler.api import deps
from app.anfler.api import api_security
from anfler.db.database import DBWrapper, message_to_job_request
from anfler.kafka_wrapper.kw import KafkaProducerWrapper
from anfler.util.helper import *

_log= lw.get_logger("anfler.api.jobs")

router = APIRouter(tags=["jobs"])


# ---------------------------------------------------------------------------
#   Utils
# ---------------------------------------------------------------------------
def __dbjob_2_apijob(job,entity):
    """Convert DBJob object to SchemaJob"""
    return api_schemas.Job(
            id=job.msg_id,
            user=job.user,
            entity=entity,
            service=job.service,
            payload_in=job.payload_in,
            payload_out=job.payload_out,
            state=job.state,
            status=job.status,
            errors=job.errors["errors"] if  "errors" in job.errors else [],
            dt_created=str(job.dt_created),
            dt_updated=str(job.dt_updated)
        )


# ---------------------------------------------------------------------------
#   Route
# ---------------------------------------------------------------------------
@router.post("/jobs/{entity}/{service}", response_model=api_schemas.JobResponse)
async def create_job(job: api_schemas.JobRequest,
                         entity: db_schemas.Entities,
                         service: str,
                         request: Request,
                         token_data = Depends(api_security.get_token_data),
                         db: DBWrapper = Depends(deps.get_db),
                         kp: KafkaProducerWrapper = Depends(deps.get_kafka_prducer),
                         ):
    """Submit a Job"""
    service =deps.check_service_name(request)

    kafka_topic = f"tributosimple-topic-{entity}"

    _log.debug(f"Creating jog for entity={entity} service={service} topic={kafka_topic} body={job}")
    message = msg.get_basic_message(header={"service":service,
                                            "fn": deps.get_fn_from_entities(entity,service),
                                            "user" : token_data.username,
                                            "auth": job.header.auth.dict(),
                                            "entity": entity,
                                            "wrap_in": "message"},
                                            payload=copy.deepcopy(job.payload))
    job_request = message_to_job_request("None", message,entity,service)
    job = await db.create_job(job_request)
    kp.send(kafka_topic, message)
    response = api_schemas.JobResponse(id=job.msg_id,
                                      service=job.service,
                                      entity=entity,state=job.state,
                                      header=api_schemas.Header(**message.get("header")).mask(),
                                      payload=message.get("payload"),
                                      status=job.status,
                                      errrors=job.errors)
    return response
# ---------------------------------------------------------------------------
#   Route
# ---------------------------------------------------------------------------
@router.get("/jobs/{entity}", response_model=List[api_schemas.Job])
async def get_jobs(entity: db_schemas.Entities,
                       service: str = None,
                       state: db_schemas.JobState = None,
                       status: int = None,
                       skip: int = 0, limit: int = 100,
                       db: DBWrapper = Depends(deps.get_db),
                       token_data = Depends(api_security.get_token_data)):
    """Get information from submited jobs for the entity (filtered by user)"""
    #_log.info(f"Connected {db.is_connected()}")
    state = int(state.value) if state else None
    jobs= await db.get_jobs(user=token_data.username, state=state, status=status, entity=entity, service=service,skip=skip,limit=limit)

    _log.debug(f"Query to '{entity}' return {len(jobs)} records")
    return [__dbjob_2_apijob(job, entity) for job in jobs]

# ---------------------------------------------------------------------------
#   Route
# ---------------------------------------------------------------------------
@router.get("/jobs/{entity}/{id}",response_model=api_schemas.Job)
async def get_jobs(id: str,
                   entity:db_schemas.Entities,
                   db:DBWrapper = Depends(deps.get_db),
                   token_data = Depends(api_security.get_token_data)):

    """Get information from job identified by *id*"""
    job = await db.get_jobs_by_id(id,user=token_data.username, entity=entity)

    if job is None:
        raise HTTPException(status_code=404, detail=f"Job with msg_id {id} not found for entity {entity}")
    return __dbjob_2_apijob(job, entity)


# ---------------------------------------------------------------------------
#   Route
# ---------------------------------------------------------------------------
@router.get("/jobs/{entity}/users/{username}",response_model=List[api_schemas.Job])
async def get_jobs(username:str,
                   entity:db_schemas.Entities,
                   service:str=None,
                   state:db_schemas.JobState=None,
                   status:int=None,
                   skip:int=0, limit:int=100,
                   token_data = Depends(api_security.get_token_data),
                   db:DBWrapper= Depends(deps.get_db)):
    """Get information from submited jobs for used *user_id*"""
    jobs = await db.get_jobs_by_user(username, entity=entity,service=service,state=state, status=status,skip=skip,limit=limit)
    return [__dbjob_2_apijob(job, entity) for job in jobs]
