import os
import time
import copy
import uuid
import random
from datetime import datetime

import signal
import anfler.util.config.cfg as cfg
from anfler.util.log.lw import init_logging, end_logging, get_logger
import anfler.util.msg.message as msg
from anfler.util.helper import dpath
import anfler.mp.threadpool as tp
from anfler.mp.helper import execute_class_method

_log = get_logger("anfler.app")

#---------------------------------------------------------------------------
def sig_keyboardInterruptHandler(signal, frame):
    global stop_loop
    _log.info(f"Signal {signal} received")
    stop_loop=True

#---------------------------------------------------------------------------
def fn1(data=None):
    rc = {"t":time.asctime()}
    #_log.info(f"Starting {threading.current_thread().name}|{threading.current_thread().native_id} - {data}")
    time.sleep(20)
    #_log.info(f"Finishing {threading.current_thread().name}|{threading.current_thread().native_id} - {rc}")
    return rc

def fn2(data=None):
    rc = {"t":time.asctime()}
    #_log.info(f"Starting {threading.current_thread().name}|{threading.current_thread().native_id} - {data}")
    time.sleep(10)
    #_log.info(f"Finishing {threading.current_thread().name}|{threading.current_thread().native_id} - {rc}")
    return rc
#---------------------------------------------------------------------------
NULL_BATCH_ID="-1_-1"
BATCH={
    "id":NULL_BATCH_ID,
    "ok":True,
    "messages":[]
}
FUNCTIONS=["fn1", "fn2", "fXX",
           "anfler.mp.dummy.DummyClass@echo",
           "anfler.mp.dummy.DummyClass@sleep",
           "anfler_afip.anfler_ccma.CCMA@run"]
FUNCTIONS_DATA=["","","",
                {"data": str(datetime.now())},
                {"sleep":30},
                {"t_s":100}
                ]
FUNCTIONS_INIT=["","","",
                {},
                {},
                {"message":{"data":{"cuit": 2095680432222,"password": "CIv16953524b222222","from": "01/01/2020","to": "01/11/2020"}},"browser": "chrome"}
                ]
MESSAGES=[
{
    "id": str(uuid.uuid4()),
    "header": {"fn": "anfler.mp.dummy.dummyclass.DummyClass@echo","user": "anfler","entity": "admin","service": "echo","method_args": {"data":"Some data"}},
    "payload": {"arg1": "init_param1", "arg2":"init_param2"}
},
{
    "id": str(uuid.uuid4()),
    "header": {"fn": "anfler.mp.dummy.dummyclass.DummyClass@sleep","user": "anfler","entity": "admin","service": "sleep", "method_args":{"sleep_time":20}},
    "payload": {}
}
]
def getData2(max_records=2):
    batch=copy.deepcopy(BATCH)
    messages = []
    batch_ok=True
    for i in range(0,max_records):
        id=random.randint(0,len(FUNCTIONS)-1)
        fn =FUNCTIONS[id]
        message = msg.get_basic_message(header={"key": id, "fn": fn}, payload=FUNCTIONS_DATA[id])

        messages.append(message)
        batch["messages"].append(message)
    batch["id"] = "x_y"
    batch["ok"] = batch_ok
    batch["messages"] = messages
    return batch

def getData(max_records=2):
    batch = copy.deepcopy(BATCH)
    messages = []
    for i in range(0,max_records):
        messages.append(random.choice(MESSAGES))
    batch["id"] = "x_y"
    batch["ok"] = True
    batch["messages"] = messages
    return batch
#---------------------------------------------------------------------------
def get_message_info(message, include_payload=False):
    partition=message.get('header').get('partition',"MISSING")
    offset=message.get('header').get('offset',"MISSING")
    return f"offset={offset}|{msg.to_string(message,payload=include_payload)}|partition=p{partition}"


if __name__ == '__main__':
    cfg.load([ "config.json"])
    init_logging(config_file="logging_test.json")
    pool = tp.RestrictedThreadPoolExecutor(**cfg.get("pool"))
    i=0
    MAX=50
    max_records=1
    jobs = {}
    while i <= MAX:
        batch = getData(cfg.get("pool.max_workers"))
        if pool.isFull():
            _log.info(f"Pool full, size={pool.getSize()}")
            time.sleep(5)
        else:
            if len(batch["messages"]) >0 :
                batch_errors=0
                _log.debug(f"Batch {batch['id']} start with {len(batch['messages'])} messages")
                jobs = {}
                for i, message in enumerate(batch["messages"]):
                    _log.debug(f"Executing msg#{i} {msg}")
                    try:
                        id = pool.submit(execute_class_method,
                                         **{"string_func":message["header"]["fn"],
                                            "init_args": {dpath(message, "header.wrap_in"):message} if dpath(message, "header.wrap_in",None) != None  else message["payload"],
                                            "method_args": dpath(message, "header.method_args", {})})

                        jobs[id] = message
                    except Exception as e:
                        _log.error(f"Error executing msg#{i} {message}. {str(e)}",stack_info=False)
                        batch_errors+=1
                try:
                    responses = pool.wait(timeout=cfg.get("pool.wait_timeout_sec"))
                    for r in responses:
                        _log.debug(f"Response from {r}")
                        jobs[r["id"]] = msg.update_message(jobs[r["id"]], status=r["status"],errors=r.get('errors', []))
                        if r["status"] != 0:
                            _log.error(f"Task={r['id']}|batch={batch['id']}|{jobs[r['id']]}")
                        else:
                            _log.info(f"Task={r['id']}|batch={batch['id']}|{jobs[r['id']]}")
                except Exception as e:
                    _log.error(f"Getting response. ({str(e)})")
                    _log.error(f"Job={id}|batch={batch['id']}|{get_message_info(message)}",exc_info=True)

                _log.info("SLEEPING....")
                time.sleep(600)

    pool.shutdown()
    _log.info("Waiting...")
    time.sleep(60)
    end_logging()