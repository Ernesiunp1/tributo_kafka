"""
Wrapper for logging package

See
    https://docs.python.org/3/howto/logging-cookbook.html
    https://docs.python.org/3.9/library/logging.config.html#configuration-dictionary-schema

Example:
    See test_logging.py

"""

import json
import re
import os
import logging
import logging.config
from collections import namedtuple

# for logging listener
logging_port=0
logging_thread=None

def init_logging(config_file=None, port=0,level=logging.INFO):
    """Initialize logging using config_file if defined, otherwise with BasicConfig
    If port!=0 open listen port
    Override variables defined in handlers , variable must be defined as {VAR}.
    For example:
              "filename": "{APP_LOG}/output2.log",
    If env varible is defined as APP_LOG=/tmp, handler will  be replaced with
        "filename": "/tmp/output2.log",

    Args:
    :param config_file: Logging file (https://docs.python.org/3/library/logging.config.html#logging.config.listen
    :param port: listen port (https://docs.python.org/3/library/logging.config.html#logging.config.listen)
    :param level: logging level
    """
    global logging_port, logging_thread
    config={}
    logging_port = port
    if config_file:
        with open(config_file, 'r', encoding="utf-8") as fd:
            config=json.load(fd)
        ## Overriding env variables in handlers
        pat =re.compile(r'^(.*){([A-Za-z0-9_]*)}(.*)$')
        for h in config["handlers"].keys():
            for k,v in config["handlers"][h].items():
                m =  pat.match(str(v))
                if m:
                    var_= m.group(2)
                    if os.environ.get(var_, None) != None :
                        config["handlers"][h][k]= str(v).replace("{"+var_+"}",os.environ[var_])
        logging.config.dictConfig(config)
        if logging_port > 0:
            logging_thread = logging.config.listen(logging_port)
            logging_thread.start()
    else:
        logging.basicConfig(level=level,
                            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        logging.root.level= level

def end_logging():
    """Stop logging listener (if it was initilized)"""
    global logging_server
    if logging_port > 0:
        logging_thread.stopListening()

def set_logger_level(logger_name, level=logging.INFO):
    """Set log level for logger"""
    logging.getLogger(logger_name).setLevel(level)


def get_logger(name):
    """Get a logger"""
    return logging.getLogger(name)


__LEVELS= namedtuple("level",["CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET"])
level=__LEVELS(CRITICAL = logging.CRITICAL,
FATAL = logging.CRITICAL,
ERROR = logging.ERROR,
WARNING = logging.WARNING,
WARN = logging.WARN,
INFO = logging.INFO,
DEBUG = logging.DEBUG,
NOTSET = logging.NOTSET)