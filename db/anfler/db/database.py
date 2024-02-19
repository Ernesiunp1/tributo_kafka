"""DB wrapper (TributoSimple)
"""
import copy
import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base



import anfler.util.log.lw as lw
import anfler.util.constants as C
from anfler.db import models
from anfler.util.helper import  dpath

_log = lw.get_logger("anfler.db")

# ---------------------------------------------------------------------------
#   Helper function
# ---------------------------------------------------------------------------
def get_model_4_entity(entity:C.ENTITIES=None):
    """Return DB models for entity entity

    Args:
        entity: Entity , see anfler.util.constants.ENTITIES

    Returns: Database model (see anfler.db.models)
    """
    if entity == None:
        return  models.JobAll
    elif entity == C.ENTITIES.AFIP:
        return  models.JobAfip
    elif entity == C.ENTITIES.AGIP:
        return  models.JobAgip
    elif entity == C.ENTITIES.ARBA:
        return  models.JobArba
    elif entity == C.ENTITIES.ADMIN:
        return  models.JobAdmin
    else:
        return models.JobAll

def message_to_job_request(job_id,message,entity,service):
    """
    Transform a BASIC_MESSAGE to database model Job
    Args:
        message: BASIC_MESSAGE dict (see anfler.util.msg.message.py)
        entity: Entity (see anfler.constants.ENTITIES)

    Returns:
        Model.JobX (see anfler.db.models.py)
    """
    data = {
        "job_id": job_id,
        "user" : dpath(message, "header.user",""),
        "service": service,
        "fn" : dpath(message, "header.fn"),
        "msg_id": dpath(message, "id"),
        "kafka_key": dpath(message, "header.key",-1),
        "kafka_offset": dpath(message, "header.offset",-1),
        "kafka_partition": dpath(message, "header.partition",-1),
        "payload_in" : copy.deepcopy(dpath(message, "payload",{})),
        "payload_out": {},
        "errors": {"errors":[]}
    }
    #return models.Job(**data)
    return get_model_4_entity(entity)(**data)

def message_to_job_response(job_id,state,message,entity):
    """
    Transform a BASIC_MESSAGE to database model Job
    Args:
        message: BASIC_MESSAGE dict (see anfler.util.msg.message.py)
        entity: Entity (see anfler.constants.ENTITIES)

    Returns:
       Database model object  (see anfler.db.models.py)
    """
    data = {
        "user" : dpath(message, "header.user",""),
        "job_id": job_id,
        "service": dpath(message, "header.service"),
        "fn" : dpath(message, "header.fn"),
        "msg_id": dpath(message, "id"),
        "kafka_key": dpath(message, "header.key",-1),
        "kafka_offset": dpath(message, "header.offset",-1),
        "kafka_partition": dpath(message, "header.partition",-1),
        "payload_out" : copy.deepcopy(dpath(message, "payload",{})),
        "errors": {"errors":dpath(message, "errors", [])},
        "status": dpath(message, "status",-1),
        "state": state
    }
    return get_model_4_entity(entity)(**data)


# ---------------------------------------------------------------------------
#   DB Jobs Wrapper
# ---------------------------------------------------------------------------
class DBWrapper():
    __DEFAULT_INIT_RETRY__ = 10
    __DEFAULT_INIT_RETRY_DELAY__ = 60
    __DEFAULT_POOL_RECYCLE__ =3600
    __DEFAULT_POOL_SIZE__ = 5
    __DEFAULT_POOL_TIMEOUT__ = 30
    def __init__(self, config):
        self._config = config
        self._init_retry_count = 0
        self._init_retry_max = self._config.get("init_retry_max", DBWrapper.__DEFAULT_INIT_RETRY__)
        self._init_retry_delay = self._config.get("init_retry_delay", DBWrapper.__DEFAULT_INIT_RETRY__)
        self._pool_recycle = self._config.get("pool_recycle", DBWrapper.__DEFAULT_POOL_RECYCLE__)
        self._pool_size = self._config.get("pool_size", DBWrapper.__DEFAULT_POOL_SIZE__)
        self._pool_timeout = self._config.get("pool_timeout", DBWrapper.__DEFAULT_POOL_TIMEOUT__)

        self.url = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}/{config['database']}"
        self._engine = create_engine(self.url, pool_recycle=self._pool_recycle, pool_size=self._pool_size)

        while self._init_retry_count < self._init_retry_max:
            try:
                self._engine = create_engine(self.url,pool_recycle=self._pool_recycle, pool_size=self._pool_size,pool_timeout=self._pool_timeout)
                self._session_local = sessionmaker(autocommit=False, autoflush=False, bind=self._engine, expire_on_commit=True)()
                self._base = declarative_base()
                self._conn = self._engine.connect()

                break
            except Exception as e:
                # sqlalchemy.exc.InterfaceError: (mysql.connector.errors.InterfaceError) 2013: Lost connection to MySQL server during query
                _log.error(f"Error initilializing db, attempt #{self._init_retry_count} of {self._init_retry_max}, sleeping {self._init_retry_delay} secs",exc_info=True)
                time.sleep(self._init_retry_delay)
                self._init_retry_count += 1

        if self.__check_db() == False:
            raise Exception(f"Cannot connect to DB after {self._init_retry_max} attempts")
        _log.info(f"Connected to {config['user']}@{config['host']}/{config['database']}")

    def __check_db(self):
        """Internal funcion to check if DB is active"""
        try:
            result = self._conn.execute(text("SELECT 1 as is_alive"))
            return  True
        except Exception as e:
            return False

    def _get_session_local(self):
        #return self._session_local
        db = self._session_local
        try:
            return db
        finally:
            db.close()

    def is_connected(self):
        if self._get_session_local().connection():
            return True
        else:
            return False

    async def create_job(self, job: models.Job):
        """Insert a new record in table jobs_<entity>
        :param job: Job object
        :return: Job object (updated)
        """
        _log.debug(f"Creating job for entity={job.entity} {str(job)}")
        sess = self._get_session_local()
        sess.add(job)
        sess.commit()
        sess.refresh(job)
        sess.close()
        return job

    def __add_default_filter(self,user=None,service=None,state=None,status=None, extra={}):
        """Internal function to add a query filters
        :param user: username (jobs_xxx.user)
        :param service: service (jobs_xxx.service)
        :param state: state (jobs_xxx.state)
        :param status: status (jobs_xxx.status)
        :param extra: Dict to add extra condition

        :return: Filter dicionary
        """
        filter = {}
        if state is not None:
            filter["state"]= int(state)
        if status is not None:
            filter["status"]=int(status)
        if service is not None:
            filter["service"] = service
        if user is not None:
            filter["user"]=user
        if len(extra) >0 :
            for k,v in extra.items():
                filter[k]= v
        return filter

    async def get_jobs(self,
                 entity:str,
                 user:str=None,
                 service:str=None,
                 state:models.JobState=None,
                 status:int=None,
                 skip: int = 0, limit: int = 100) :
        """Query table jobs_<entity>
        :param user: username (jobs_xxx.user)
        :param service: service (jobs_xxx.service)
        :param state: state (jobs_xxx.state)
        :param status: status (jobs_xxx.status)
        :param entity: entity (anfler.util.constants.ENTITIES)
        :param skip: offset (https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.offset)
        :param limit: limit (https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.limit)

        :return List of Jobs
        """

        filter = self.__add_default_filter(user=user,state=state,status=status,service=service)
        rows = None
        if len(filter) > 0:
            rows = self._get_session_local().query(get_model_4_entity(entity)).filter_by(**filter).offset(skip).limit(limit).all()
        else:
            rows = self._get_session_local().query(get_model_4_entity(entity)).offset(skip).limit(limit).all()
        _log.debug(f"#rows={len(rows)}")
        if _log.isEnabledFor(lw.level.DEBUG):
            for r in rows:
                _log.debug(r.__dict__)
        return rows

    async def get_jobs_by_id(self,
                       id:str,
                       entity,
                       user:str = None) -> models.Job:
        """Query an specific job
        :param id: Job MsgId (jobs_xxxx.msg_id)
        :param user: username (jobs_xxx.user)
        :param entity: entity (anfler.util.constants.ENTITIES)

        :return Job
        """
        filter = self.__add_default_filter(user=user,extra={"msg_id":id})
        rows = None
        try:
            rows= self._get_session_local().query(get_model_4_entity(entity)).filter_by(**filter).one()
        except NoResultFound as nrf:
            _log.warn(f"Job with job_id={id} for entity={entity} not found")
        return rows


    async def get_jobs_by_user(self,
                         user:str,
                         entity,
                         service: str = None,
                         state:models.JobState=None,
                         status:int=None,
                         skip: int = 0, limit: int = 100
                         ) -> [models.Job]:
        """Query table jobs_<entity> filtering by user
        :param user: username (jobs_xxx.user)
        :param service: service (jobs_xxx.service)
        :param state: state (jobs_xxx.state)
        :param status: status (jobs_xxx.status)
        :param entity: entity (anfler.util.constants.ENTITIES)
        :param skip: offset (https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.offset)
        :param limit: limit (https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.limit)

        :return List of Jobs for the user
        """
        filter = self.__add_default_filter(user=user, service=service,state=state, status=status)
        rows = self._get_session_local().query(get_model_4_entity(entity)).filter_by(**filter).all()
        return rows

    async def get_jobs_by_status(self,
                           entity,
                           user=None,
                           service: str = None,
                           status:int = 0 ,
                           skip: int = 0, limit: int = 100) -> [models.Job]:
        """Query table jobs_<entity> filtering by status
        :param user: username (jobs_xxx.user)
        :param service: service (jobs_xxx.service)
        :param status: status (jobs_xxx.status)
        :param entity: entity (anfler.util.constants.ENTITIES)
        :param skip: offset (https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.offset)
        :param limit: limit (https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.limit)

        :return List of Jobs
        """
        filter = self.__add_default_filter(user=user,  status=status)
        return self._get_session_local().query(get_model_4_entity(entity)).filter_by(**filter).offset(skip).limit(limit).all()

    async def get_jobs_by_state(self,
                          entity,
                          user:str=None,
                          service: str = None,
                          state:models.JobState=models.JobState.pending,
                          skip: int = 0, limit: int = 100) -> [models.Job]:
        """Query table jobs_<entity> filtering by state
        :param user: username (jobs_xxx.user)
        :param service: service (jobs_xxx.service)
        :param state: state (jobs_xxx.state)
        :param entity: entity (anfler.util.constants.ENTITIES)
        :param skip: offset (https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.offset)
        :param limit: limit (https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.limit)

        :return List of Jobs
        """
        filter = self.__add_default_filter(user=user,state=state)
        return self._get_session_local().query(get_model_4_entity(entity)).filter_by(**filter).offset(skip).limit(limit).all()

    def update_job(self, job,entity):
        """Update a Job record
        :param job
        :param entity: entity (anfler.util.constants.ENTITIES)

        :return Job Object (updated)
        """
        _log.debug(f"Updating job for entity={entity} job_id={str(job.job_id)} msg_id={job.msg_id} status={job.status} state={job.state}")
        # If record no found, raise orm_exc.NoResultFound
        try:
            session = self._get_session_local()
            q: models.Job = session.query(get_model_4_entity(entity)).filter_by(msg_id=job.msg_id).one()
            q.msg_id = job.msg_id
            q.job_id = job.job_id
            q.status = job.status
            q.state = job.state
            q.errors = job.errors
            q.kafka_key = job.kafka_key
            q.kafka_offset = job.kafka_offset
            q.kafka_partition =  job.kafka_partition
            q.payload_out = job.payload_out
            session.add(q)
            session.commit()
            session.refresh(q)
            return q
        except NoResultFound as nrf:
            _log.warn(f"Job with job_id={job.job_id} for entity={entity} not found")
            raise Exception(f"Job with job_id={job.job_id} for entity={entity} not found")


    def get_services(self,entity=None) -> [models.JobServices]:
        """List services (table jobs_services)
        :param entity
        :return List of services
        """
        filter = {}
        if entity :
            filter["entity"] = entity
        return self._get_session_local().query(models.JobServices).filter_by(**filter).order_by(models.JobServices.entity, models.JobServices.service).all()
