import sys
import time
import copy
import random
from anfler.db import models, schemas
from anfler.db.database import  DBWrapper, message_to_job_request
import anfler.util.config.cfg as cfg
import anfler.util.log.lw as lw
import anfler.util.msg.message as msg
from anfler.util.helper import dpath
import anfler.util.constants as C
from pprint import pprint


_log = lw.get_logger("anfler.db")


def print_res(rows,label=None):
    _rows = rows
    if rows == None or (isinstance(rows,list) and len(rows) ==0):
        _log.warning("Empty response")
        return
    elif isinstance(rows,list) :
        _rows = rows
    else:
        _rows = [rows]
    if label:
        _log.info(f"{label}")
    for i,row in enumerate(_rows):
        #_log.info(f"#{i:02d} {row.id:03d} {row.user:10s} {row.state} {row.status}  {row.errors} ")
        _log.info(f"#{i:02d} {row.id:03d} {row.user:10s} {row.state} {row.status} {row.dt_created} {row.dt_updated} {row.errors} ")




if __name__ == '__main__':
    lw.init_logging("logging-test.json")
    cfg.load("config-test.json")
    db = DBWrapper(cfg.get("db"))

    service = C.ENTITIES.AFIP

    _log.info("=======  QUERY ======")

    rows = db.get_jobs(entity=C.ENTITIES.AFIP)
    print_res(rows)
    _log.info("=======  CREATE =====")
    message = msg.get_basic_message(header={"fn": "anfler_afip.anfler_ccma.CCMA@run",
                                            "auth": {"type": "basic", "cuit": random.randint(10000000, 99999999),"password": "CIv16953524b"},
                                            "entity": C.ENTITIES.AFIP,
                                            "service": "dummy",
                                            "offset":99,
                                            "partition":1},
                                   payload={"message":{"data":{"from": "01/01/2020","to": "01/11/2020", "t_s":2}}})



    job_request = message_to_job_request(None,message,C.ENTITIES.AFIP, "dummy")
    job = db.create_job(job_request)
    _log.info(f"{job.job_id} {job.dt_created}")

    _log.info("=======  QUERY by JOB ======")
    print_res(db.get_jobs_by_id(job.job_id,entity=C.ENTITIES.AFIP))

    _log.info("=======  QUERY by STATE 0 ======")
    print_res(db.get_jobs_by_state(state=0,entity=C.ENTITIES.AFIP))

    _log.info("=======  QUERY by STATE 1 ======")
    print_res(db.get_jobs_by_state(state=1,entity=C.ENTITIES.AFIP))

    _log.info("=======  QUERY by USER 1 ======")
    print_res(db.get_jobs_by_user("71791967",entity=C.ENTITIES.AFIP))


    _log.info("=======  UPDATE =====")
    job_request.status=9
    job_request.errors = ["error1", "error2"]
    db.update_job(job_request,entity=C.ENTITIES.AFIP)
    print_res(rows)
    _log.info("=======  QUERY ======")
    print_res(db.get_jobs(entity=C.ENTITIES.AFIP))
