"""Dummy class for ThreadPool tester"""
import time
from datetime import datetime
import anfler.util.log.lw as lw


_log= lw.get_logger("anfler.mp.dummy")

class DummyClass():
    def __init__(self, arg1="init_param1", arg2="init_param2"):
        _log.info(f"arg1={arg1} arg2={arg2}")

    def echo(self, data):
        res ={"data_old":data, "data_new": str(datetime.now())}
        _log.info(f"Received <{data}>, response={res}")
        return res

    def sleep(self, sleep_time=10):
        _log.info(f"Start sleeping {sleep_time} sec")
        time.sleep(sleep_time)
        _log.info(f"End sleeping")
        return {"rc":"OK"}

