"""Dummy service to testing
"""
from datetime import datetime
import platform
import anfler.util.log.lw as lw
import anfler.util.msg.message as msg
from anfler.util.helper import dpath
_log = lw.get_logger("anfler.app")

class DummyService():
    """
    Dummy service to testing
    """
    def __init__(self, message):
        self.message = dpath(message, "payload", "")

    def echo(self, message={}):
        """Echo message

        :param message: BASIC_MESSAGE dict
        :return: BASIC_MESSAGE dict
        {
            "payload":  {"output": { "hostname":<hostname>, "datetime_utc": <server datetime utc>, "input_data": <received data>}}
        }
        """
        _log.info(f"Received {message}")
        response = msg.get_basic_message(payload={"output": {"hostname": str(platform.node()), "datetime_utc": str(datetime.utcnow()), "input_data": str(self.message)}})
        response = msg.update_message(response, status=0)
        #_log.debug(f"Return {response}")
        return response


    def error(self, message={}):
        """Return error

        :param message: BASIC_MESSAGE dict
        :return: BASIC_MESSAGE dict
        {
            "status": 99
            "errors": ["Some error 1","Some error 2"]
        }
        """
        _log.info(f"Received {message}")
        response = msg.get_basic_message(payload={})
        dummy_errors= ["Some error 1","Some error 2"]
        response = msg.update_message(response, errors=dummy_errors, status=99)
        #_log.debug(f"Return {response}")
        return response


