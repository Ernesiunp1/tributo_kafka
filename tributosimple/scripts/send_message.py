#!/usr/bin/env python3
import sys
import os
import uuid
import json
import copy
import argparse
import random
import anfler.util.log.lw as lw
import anfler.util.config.cfg as cfg
import anfler.util.msg.message as msg
from anfler.kafka_wrapper.kw import KafkaProducerWrapper
from anfler.db.database import DBWrapper, message_to_job_request, message_to_job_response
from anfler.util.helper import dpath

import anfler.util.constants as C
_log = lw.get_logger("anfler.app")

#---------------------------------------------------------------------------
def override_values(message, data=None):
    message_ = copy.deepcopy(message)
    if dpath(message_,"id") == "REGENERATE":
        message_["id"] = str(uuid.uuid4())

    values={}
    for d in data:
        values[d.split("=")[0]]=d.split("=")[1]
    if dpath(message_, "header.auth.cuit","") == "REGENERATE":
        message_["header"]["auth"]["cuit"] = int(values["header.auth.cuit"])
    if dpath(message_, "header.auth.password","") == "REGENERATE":
        message_["header"]["auth"]["password"] = values["header.auth.password"]
    return message_

def load_json(filename):
    message={}
    _log.info(f"Reading {filename}")
    with open(filename) as json_file:
        message = json.load(json_file)

    return message
#---------------------------------------------------------------------------
def list_message_files():
    files=[]
    for f in os.listdir():
        if f.startswith("msg-") and f.endswith(".json"):
            files.append(f)
    return files
#---------------------------------------------------------------------------
def load_messages(filenames):
    messages=[]
    try:
        if isinstance(filenames,str) and filenames == "all":
            for f in list_message_files():
                messages.append(load_json(f))
        else:
            for f in filenames:
                messages.append(load_json(f))
    except Exception as e:
        _log.error(f"Got some error, ignoring {str(e)}")
    return messages

def get_version():
    return [f"{SCRIPT_NAME} v{SCRIPT_VERSION} ({SCRIPT_DATE})",f"Python version {sys.version}"]
#---------------------------------------------------------------------------
#   Command args
#---------------------------------------------------------------------------
SCRIPT_NAME="send_message.py"
SCRIPT_DESCRIPTION = 'Simple client'
SCRIPT_VERSION ="0.1.0"
SCRIPT_DATE="2021-01-07"
description_message = ""

example_usage = """
Example:
- Send 10 messages (choosed from msg-afip-*)
send_message.py -n 10 -f msg-afip-* -d header.auth.cuit=1212121212 header.auth.password=xxxxxx

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
                        default="config_test.json")

    parser.add_argument("-l", "--log",
                        help="Logging configuration",
                        default="logging_test.json")

    parser.add_argument("-f", "--files",
                        help="Messages files",
                        nargs='*',
                        default="all")

    parser.add_argument("-n", "--num",
                        help="Number of messages to sent",
                        type=int,
                        default=1)

    parser.add_argument("-r", "--random",
                        help="Choose randomly messages",
                        action='store_true')

    parser.add_argument("-v", "--version",
                        help="Show script version",
                        action='store_true')

    parser.add_argument("-d", "--data",
                        help="Override data\n"
                             "Format: header.auth.cuit=value header.auth.password=value",
                        nargs='*',
                        default="")

    args = parser.parse_args()
    if args.version:
        print(get_version()[0])
        print(get_version()[1])
        sys.exit(0)
    return args

#---------------------------------------------------------------------------
#  Main
#---------------------------------------------------------------------------
if __name__ == '__main__':
    args = parse_args()
    lw.init_logging(args.log,level=lw.level.DEBUG)
    cfg.load(args.config)
    kw = KafkaProducerWrapper(cfg.get("kafka"))
    db = DBWrapper(cfg.get("db"))

    messages=load_messages(args.files)
    if len(messages) == 0:
        _log.error("Ops, no messages loaded :-(")
        sys.exit(0)

    j=0
    for i in range(1,args.num + 1):
        if args.random:
            message = override_values(random.choice(messages),args.values)
        else:
            message = override_values(messages[j],args.data)
            j+=1
            if j >= len(messages):
                j=0
        #message,job_request = get_message()
        job_request = message_to_job_request("None", message, message["header"]["entity"], message["header"]["service"])
        id=dpath(message, 'id')
        entity=dpath(message, 'header.entity')
        service=dpath(message, 'header.service')
        #_log.info(f"Sending service_type={dpath(message, 'header.service')} {msg.to_string(message, header=True, payload=False)}")
        job = db.create_job(job_request)
        topic="tributosimple-topic-"+dpath(message, "header.entity")
        res = kw.send(topic, message)

        _log.info(f"#{i:02} Sent id={id} entity/service={entity}/{service} {res}")
    _log.info(f"Sent {i} messages")
