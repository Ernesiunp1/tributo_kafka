import os
from fastapi import FastAPI

# from . import crud, deps, models, schemas, security
# from .api import items, users
# from .database import SessionLocal, engine
# from .settings import settings

from app.anfler.api import deps, api_security
from app.anfler.api import jobs
from app.anfler.api import default
from app.anfler.api import admin
from anfler.db.database import DBWrapper

import anfler.kafka_wrapper.kw as kw
import anfler.util.log.lw as lw
import anfler.util.config.cfg as cfg

_log= lw.get_logger("anfler.api")

# ---------------------------------------------------------------------------
#   Global variables
# ---------------------------------------------------------------------------
db:DBWrapper = None
kp:kw.KafkaProducerWrapper = None


# ---------------------------------------------------------------------------
#   Documentation
# ---------------------------------------------------------------------------
TAGS_METADATA = [
    {
        "name": "default",
        "description": "Dummy operations"
    },
    {
        "name": "jobs",
        "description": "Operation with jobs"
    }
]
ANFLER_API_DOC={
    "title" : "TributSimple API",
    "description" : "API de gestión contable/impositiva a monotributistas",
    "version" : "0.0.1",
    "openapi_tags": TAGS_METADATA
}

# def init_deps():
#     global db, kp
#     db =  DBWrapper(cfg.get("db"))
#     s =db.get_services()
#     print(s)
#     kp = kw.KafkaProducerWrapper(cfg.get("kafka"))
#     lw.init_logging(os.environ["APP_CONFIG_LOG"], level=lw.level.INFO)


# ---------------------------------------------------------------------------
#   App creation
# ---------------------------------------------------------------------------
def create_app():
    global  db, kp
    print(f"Creating app")

    cfg.load(["/app/anfler-tributosimple-api/etc/config.json"])
    api_security.jwt_set_config(cfg.get("jwt"))

    app = FastAPI(**ANFLER_API_DOC)
    print(f"Created")
    #init_deps()
    db =  DBWrapper(cfg.get("db"))

    kp = kw.KafkaProducerWrapper(cfg.get("kafka"))
    lw.init_logging(os.environ["APP_CONFIG_LOG"], level=lw.level.INFO)

    deps.load_registry(db)
    deps.set_db(db)
    deps.set_kafka_prducer(kp)
    app.include_router(admin.router, tags=["admin"])
    app.include_router(jobs.router, tags=["jobs"])
    app.include_router(default.router, tags=["default"])

    return app
#

# @app.on_event("startup")
# def startup_event():
#     print(f"Starting app")
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     print(f"Stoping app")
app = create_app()


