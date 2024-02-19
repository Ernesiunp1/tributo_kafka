"""Database models"""
import enum
from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

import anfler.util.constants as C


Base = declarative_base()


class JobState(enum.Enum):
    pending:int  = int(C.JOBS_STATE.PENDING)
    finished:int = int(C.JOBS_STATE.FINISHED)
    all:int  = -1

class Job():
    """Base class for jobs table"""
    id = Column(Integer,primary_key=True, index=True)
    msg_id = Column(String, nullable=True)
    user = Column(String, default="UNKNOWN", nullable=False)
    state = Column(Integer,default=C.JOBS_STATE.PENDING, nullable=False)
    service = Column(String, default="UNKNOWN", nullable=False)
    fn = Column(String, nullable=False)
    payload_in  = Column(JSON, nullable=False)
    payload_out  = Column(JSON, nullable=False)
    status = Column(Integer,default=C.ERRORS_CDDE.OK, nullable=False)
    errors  = Column(JSON, nullable=False)
    job_id = Column(String, nullable=True)
    kafka_key = Column(String, nullable=True)
    kafka_offset = Column(Integer,default=-1, nullable=False)
    kafka_partition = Column(Integer,default=-1, nullable=False)
    dt_created =Column(DateTime(timezone=True), default=func.now(), nullable=False)
    dt_updated =Column(DateTime(timezone=True), onupdate=func.now() , nullable=False)

class JobAfip(Base,Job):
    """Class for table jobs_afip"""
    __tablename__ = "jobs_afip"
    entity = Column(String, default=C.ENTITIES.AFIP, nullable=False)

class JobAgip(Base,Job):
    """Class for table jobs_agip"""
    __tablename__ = "jobs_agip"
    entity = Column(String, default=C.ENTITIES.AGIP, nullable=False)

class JobArba(Base,Job):
    """Class for table jobs_arba"""
    __tablename__ = "jobs_arba"
    entity = Column(String, default=C.ENTITIES.ARBA, nullable=False)

class JobAll(Base,Job):
    __tablename__ = "jobs"
    entity = Column(String, default=C.ENTITIES.ALL, nullable=False)

class JobAdmin(Base,Job):
    __tablename__ = "jobs_admin"
    entity = Column(String, default=C.ENTITIES.ADMIN, nullable=False)
"""Class for table jobs_afip"""

class JobServices(Base):
    """Class for table jobs_services"""
    __tablename__ = "jobs_services"
    id = Column(Integer, primary_key=True, index=True)
    fn = Column(String, nullable=False)
    service = Column(String, default="UNKNOWN", nullable=False)
    entity = Column(String, default=C.ENTITIES.ADMIN, nullable=False)
