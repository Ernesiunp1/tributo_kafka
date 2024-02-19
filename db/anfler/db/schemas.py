"""Database schemas"""

from datetime import datetime
from enum import Enum, IntEnum
from pydantic import BaseModel
from typing import List, Dict,Optional



import anfler.util.constants as C

class Entities(str, Enum):
    """Entities"""
    afip = "afip"
    arba = "arba"
    agip = "agip"
    admin = "admin"



class JobState(str  , Enum):
    """Jobs States """
    # pending = C.JOBS_STATE.PENDING
    # finished = C.JOBS_STATE.FINISHED
    pending = 0
    finished = 1

class Job(BaseModel):
    """Job"""
    id: Optional[int] = None
    job_id: str = C.DEFAULT_EMPTY
    user: str = C.DEFAULT_EMPTY
    state: int= C.JOBS_STATE.PENDING
    fn: str = C.DEFAULT_EMPTY
    status: int = C.ERRORS_CDDE.OK
    errors: Optional[Dict] = None
    msg_id: str = C.DEFAULT_EMPTY
    kafka_key: str = C.DEFAULT_EMPTY
    kafka_offset: int = -1
    kafka_partition: int = -1
    payload_in: Optional[Dict] = None
    payload_out: Optional[Dict] = None
    dt_created: Optional[datetime]
    dt_updated: Optional[datetime]
    class Config:
        orm_mode = True



