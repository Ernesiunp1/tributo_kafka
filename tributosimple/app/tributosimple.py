"""
Application TributoSimple
"""




import os
import json
import time
import copy
import argparse
import signal
###
import threading
import sys
import app._about as about
import anfler.util.config.cfg as cfg
import anfler.util.msg.message as msg
import anfler.util.log.lw as lw
from anfler.util.helper import *
import anfler.mp.threadpool as tp
#from anfler.mp.helper import import_modules
from anfler.mp.helper import execute_class_method

import anfler.kafka_wrapper.kw as kw
#import anfler.db.db_job as dbj
import anfler.db.database as db
import  anfler.util.constants as C


_log = lw.get_logger("anfler.app")
_log_stat = lw.get_logger("anfler.app.stat")

# Global stop flag
done=False

#---------------------------------------------------------------------------
def get_version():
    python_version=sys.version.replace('\n','')
    return [f"{SCRIPT_NAME} v{SCRIPT_VERSION} ({SCRIPT_DATE})",f"Python version {python_version}"]
#---------------------------------------------------------------------------
#   Command args
#---------------------------------------------------------------------------
SCRIPT_NAME="tributosimple.py"
SCRIPT_DESCRIPTION = 'Tributo Simple'
SCRIPT_VERSION = about.__version__
SCRIPT_DATE= about.__date__
description_message = about.__description__

example_usage = """
Examples: TBD
"""
#---------------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(prog=SCRIPT_NAME,
                                     description=description_message,
                                     epilog=example_usage,
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-c", "--config",
                        help="Configuration files (JSON format)",
                        nargs='*',
                        default="config.json")

    parser.add_argument("-l", "--log",
                        help="Logging configuration",
                        default="logging.json")

    parser.add_argument("-v", "--version",
                        help="Show script version",
                        action='store_true')

    args = parser.parse_args()
    if args.version:
        print(get_version()[0])
        print(get_version()[1])
        sys.exit(0)

    return args

#---------------------------------------------------------------------------
#   Signals
#---------------------------------------------------------------------------
def sig_InterruptHandler(signum, frame):
    global done
    #signal.signal(signal.SIGUSR1, signal.SIG_IGN)
    _log.info(f"Signal {signum} received")
    #signal.signal(signal.SIGINT, default_signal_handler)
    done=True
    sys.exit()

default_signal_handler_sigterm=None
default_signal_handler_sigint=None
def init_signals():
    global  default_signal_handler_sigterm,default_signal_handler_sigint
    default_signal_handler_sigterm = signal.getsignal(signal.SIGTERM)
    signal.signal(signal.SIGTERM, sig_InterruptHandler)

    default_signal_handler_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, sig_InterruptHandler)

def remove_signals():
    global default_signal_handler_sigterm, default_signal_handler_sigint
    signal.signal(signal.SIGTERM, default_signal_handler_sigterm)
    signal.signal(signal.SIGINT, default_signal_handler_sigint)


def get_message_info(message, include_payload=False,include_error=True):
    partition= dpath(message, "header.partition",-1)
    offset= dpath(message,"header.offset",-1)
    return f"offset={offset}|{msg.to_string(mask_data(message),payload=include_payload,errors=include_error)}|partition=p{partition}"

#---------------------------------------------------------------------------
#   Main
#---------------------------------------------------------------------------
def main(args):
    global  done
    #signal.pause()
    # ---------------------------------------------------------------------------
    #   Config and logging
    # ---------------------------------------------------------------------------
    # Try first loading from file
    if "APP_CONFIG_FILE" in os.environ:
        cfg.load([os.environ["APP_CONFIG_FILE"]],ignore_errors=True)
    if args.config :
        cfg.load(args.config,ignore_errors=True)

    cfg.load_from_env(["KAFKA_CONFIG","DB_CONFIG", "POOL_CONFIG"],ignore_errors=True)
    lw.init_logging(args.log,port=cfg.get("logging.logging_port",0,True),level=lw.level.INFO)

    _log.info(get_version()[0])
    _log.info(get_version()[1])
    _log.info(f"Starting pid={os.getpid()}")
    _log.info(f"Using configuration file {args.config}")
    _log.info(f"Using logging configuration file {args.log}")


    # ---------------------------------------------------------------------------
    #   Kafka Wrapper
    # ---------------------------------------------------------------------------
    _log.info("Initializing Kafka client...")
    kc = kw.KafkaConsumerWrapper(cfg.get("kafka"))

    # ---------------------------------------------------------------------------
    #   DB Wrapper
    # ---------------------------------------------------------------------------
    _log.info("Initializing DB client...")
    dbw =  db.DBWrapper(cfg.get("db"))
    # ---------------------------------------------------------------------------
    _log.info("Initializing pool...")
    pool = tp.RestrictedThreadPoolExecutor(**cfg.get("pool"))

    # ---------------------------------------------------------------------------
    #   Main Loop
    # ---------------------------------------------------------------------------
    _log.info("Starting loop...")

    batch_error = 0

    LOOP_COUNTER=10
    loop_counter=LOOP_COUNTER
    jobs = {}
    while done == False:
        # There should not be pending jobs, if so timeout must be adjusted
        #
        if pool.pending_jobs() > 0:
            pool.kill_childs(cfg.get("pool.child_process_names"))

        # CONSUME FROM KAFKA
        batch = kc.poll()
        kc.print_messages(batch)
        batch_errors = 0
        # Print this message every 10 iterations if no messages
        if len(batch['messages']) == 0:
            if loop_counter <= 0 :
                _log.info(f"No messages received after {LOOP_COUNTER} kafka pool iterations")
                loop_counter = LOOP_COUNTER
            else:
                loop_counter -= 1
            continue
        _log.info(f"Batch {batch['id']} messages={len(batch['messages'])} pending_messages={len(jobs)} pending_jobs={pool.pending_jobs()}")
        for k, v in jobs.items():
            _log.info(f"jobid={k} id={v['id']}")
        # SUBMIT JOBS
        for i, message in enumerate(batch["messages"]):
            _log.debug(f"Executing msg#{i}|batch={batch['id']}|{get_message_info(message)}|{mask_data(message.get('payload',''))}")
            id = None
            try:
                id = pool.submit(execute_class_method,
                                 **{"string_func": message["header"]["fn"],
                                    "init_args": {dpath(message, "header.wrap_in"):message} if dpath(message, "header.wrap_in",None) != None  else message["payload"],
                                    "method_args": dpath(message, "header.method_args", {})
                                    })
                
                _log.debug(f"Job={id}|batch={batch['id']}|id={message['id']} submited")
                jobs[id] = message
            except Exception as e:
                _log.error(f"Job={id}|batch={batch['id']}|{get_message_info(message)}")
                dbjob = db.message_to_job_response(message['id'],C.JOBS_STATE.FINISHED, message)
                job_service=dpath(message,"header.job_service",C.JOB_SERVICES.ALL)
                dbw.update_job(dbjob,job_service=job_service)
                batch_errors += 1

        # WAIT FOR JOBS
        try:
            # Get any delayed task
            responses = pool.wait(timeout=cfg.get("pool.wait_timeout_sec"))
            for r in responses:
                #_log.debug(f"Raw future response {r}")
                # First check any errors from wait()
                if r["status"] != 0:
                    # wait() executed and fails
                    jobs[r["id"]] = msg.update_message_from(jobs[r["id"]], r,["status", "payload", "errors"])
                else:
                    # Get details from wrapper BASIC_MESSAGE included in payload
                    jobs[r["id"]] = msg.update_message_from(jobs[r["id"]],r.get("payload",{}),["status","payload","errors"])

                # Check status and log
                if jobs[r["id"]]["status"] != 0:
                    _log.error(f"Response from Job={r['id']}|batch={batch['id']}|{get_message_info(jobs[r['id']],include_payload=False,include_error=True)}")
                else:
                    _log.info(f"Response from Job={id}|batch={batch['id']}|{get_message_info(jobs[r['id']] ,include_payload=False)}")
                    _log.debug(f"Response from Job={id}|batch={batch['id']}|{get_message_info(jobs[r['id']])}")
                entity = dpath(jobs[r["id"]], "header.entity", C.ENTITIES.ALL)
                dbjob = db.message_to_job_response(r["id"],C.JOBS_STATE.FINISHED,jobs[r["id"]],entity)

                dbw.update_job(dbjob,entity=entity)
                del jobs[r["id"]]
        except Exception as e:
            _log.error(f"Got some error. ({str(e)})",exc_info=True)

        # ---------------------------------------------------------------------------
        kc.commit()
    # ---------------------------------------------------------------------------
    #   Close...
    # ---------------------------------------------------------------------------
    pool.shutdown()
    # ---------------------------------------------------------------------------
    #   Kafka
    # ---------------------------------------------------------------------------
    kc.close()
    # ---------------------------------------------------------------------------
    #   Logging
    # ---------------------------------------------------------------------------
    lw.end_logging()
    _log.info(f"Aplication end, pid={os.getpid()}")

if __name__ == '__main__':
    args = parse_args()
    # ---------------------------------------------------------------------------
    #   Signal handler
    # ---------------------------------------------------------------------------
    init_signals()
    print(f"Starting main thread")
    main_thd=threading.Thread(target=main, args=(args,),daemon=True,name='anfler_main')
    main_thd.start()
    main_thd.join()
    remove_signals()
    print(f"Finishing app")
    sys.exit(0)
