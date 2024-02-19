"""
Application TributoSimple (API)
"""

import argparse
import os
import sys


from fastapi import Depends, FastAPI, HTTPException

import app.anfler.api._about as about
import app.anfler.api.api_doc as doc
import anfler.kafka_wrapper.kw as kw
import anfler.util.log.lw as lw
import anfler.util.config.cfg as cfg


from app.anfler.api import (
    admin,
    default,
    deps,
    jobs
)
from anfler.db.database import DBWrapper



_log = lw.get_logger("anfler.api")
#---------------------------------------------------------------------------
def get_version():
    python_version=sys.version.replace('\n','')
    return [f"{SCRIPT_NAME} v{SCRIPT_VERSION} ({SCRIPT_DATE})",f"Python version {python_version}"]
#---------------------------------------------------------------------------
#   Command args
#---------------------------------------------------------------------------
SCRIPT_NAME="anfler_api.py"
SCRIPT_DESCRIPTION = about.__description__
SCRIPT_VERSION = about.__version__
SCRIPT_DATE= about.__date__
description_message = about.__description__
description_message = ""

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
                        nargs='*')

    parser.add_argument("-l", "--log",
                        help="Logging configuration")

    parser.add_argument("-v", "--version",
                        help="Show script version",
                        action='store_true')

    #a
    try:
        #args = parser.parse_known_args(['--config','--log','--version'])
        args = args = parser.parse_args()
    except  Exception as e:
        print("OPS")
        print(e)
    if args.version:
        print(get_version()[0])
        print(get_version()[1])
        sys.exit(0)

    return args


# ---------------------------------------------------------------------------
#   Global variables
# ---------------------------------------------------------------------------
db= None
kp= None

#---------------------------------------------------------------------------
#   Main
#---------------------------------------------------------------------------
def main():
    global db, kp
    #signal.pause()
    # ---------------------------------------------------------------------------
    #   Config and logging
    # ---------------------------------------------------------------------------
    args_config = os.environ.get("APP_CONFIG_FILE",None)
    if args_config:
        cfg.load([args_config],ignore_errors=True)
    else:
        print(f"Please add env variable APP_CONFIG_FILE=<full path to config.json>")
        sys.exit(1)

    # if args.config :
    #     cfg.load(args.config,ignore_errors=True)
    #     args_config = args.config

    args_log = os.environ.get("APP_CONFIG_LOG_FILE",None)
    if args_log:
        lw.init_logging(args_log,port=cfg.get("logging.logging_port",0,True),level=lw.level.INFO)
    else:
        print(f"Please add env variable APP_CONFIG_LOG_FILE=<full path to logging.json>")
        sys.exit(1)
    #if args.log :
    #    lw.init_logging(args.log,port=cfg.get("logging.logging_port",0,True),level=lw.level.INFO)
    #    args_log = args.log

    _log.info(get_version()[0])
    _log.info(get_version()[1])
    _log.info(f"Starting pid={os.getpid()}")
    _log.info(f"Using configuration file {args_config}")
    _log.info(f"Using logging configuration file {args_log}")

    # ---------------------------------------------------------------------------
    #   DB Wrapper
    # ---------------------------------------------------------------------------
    _log.info("Initializing DB client...")
    db = DBWrapper(cfg.get("db"))
    # ---------------------------------------------------------------------------
    #   Kafka Wrapper
    # ---------------------------------------------------------------------------
    kp = kw.KafkaProducerWrapper(cfg.get("kafka"))
    # ---------------------------------------------------------------------------
    #   Main App
    # ---------------------------------------------------------------------------
    _log.info("Starting app...")
    app = FastAPI(**doc.ANFLER_API_DOC)
    deps.load_registry(db)
    deps.set_db(db)
    deps.set_kafka_prducer(kp)
    deps.init_security()
    app.include_router(admin.router, tags=["admin"])
    app.include_router(jobs.router, tags=["jobs"])
    app.include_router(default.router, tags=["default"])

    return app

    # ---------------------------------------------------------------------------
    #   Close...
    # ---------------------------------------------------------------------------

    # ---------------------------------------------------------------------------
    #   Logging
    # ---------------------------------------------------------------------------
    lw.end_logging()
    _log.info(f"Aplication end, pid={os.getpid()}")

# if __name__ == '__main__':
#     args = parse_args()
#     # ---------------------------------------------------------------------------
#     #   Signal handler
#     # ---------------------------------------------------------------------------
#     #init_signals()
#     print(f"Starting main thread")
#     main()
#     #remove_signals()
#     print(f"Finishing app")
#     sys.exit(0)


app = main()

#app = main(None)



