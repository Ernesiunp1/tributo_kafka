

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials

import app.anfler.api.api_security
import anfler.util.log.lw as lw
import anfler.util.config.cfg as cfg
import anfler.util.jwt.jwt_helper as jwtw

# ---------------------------------------------------------------------------
#   Global objects
# ---------------------------------------------------------------------------
_log= lw.get_logger("anfler.api.deps")

db_client_=None
kafka_producer= None

SERVICES_REGISTRY ={}


# ---------------------------------------------------------------------------
#   Verification functions for dependency injection
# ---------------------------------------------------------------------------
# security_basic = None
# security_jwt = None


# ---------------------------------------------------------------------------
#   Getter/Setter function for dependency injection
# ---------------------------------------------------------------------------
def get_db():
    return db_client_

def set_db(db):
    global db_client_
    db_client_ = db

def get_kafka_prducer():
    return kafka_producer

def set_kafka_prducer(kp):
    global kafka_producer
    kafka_producer = kp


def load_registry(db):
    global  SERVICES_REGISTRY
    services = db.get_services()
    for s in services:
        if s.entity in SERVICES_REGISTRY:
            SERVICES_REGISTRY[s.entity][s.service] = s.fn
        else:
            SERVICES_REGISTRY[s.entity] = {s.service : s.fn}


def init_security():
    global security_basic, security_jwt
    jwtw.jwt_set_config(cfg.get("jwt"))

def  check_entity_name(req:Request):
    global SERVICES_REGISTRY
    entity = req.path_params.get("entity","")
    if entity not in SERVICES_REGISTRY :
        raise HTTPException (status_code=404, detail=f"Entity '{entity}' not defined")
    else:
        return entity


def  check_service_name(req:Request):
    global SERVICES_REGISTRY
    entity = req.path_params.get("entity","")
    service = req.path_params.get("service","")
    if entity not in SERVICES_REGISTRY or service not in SERVICES_REGISTRY[entity]:
        raise HTTPException (status_code=404, detail=f"Service name '{service}' not defined for '{entity}")
    else:
        return service

def get_fn_from_entities(entity,service):
    """Return function name that map to <entity>_<service_name>

    :param entity: entity
    :param service: service name
    :return: Function name
    """
    global SERVICES_REGISTRY
    return SERVICES_REGISTRY.get(entity).get(service)
