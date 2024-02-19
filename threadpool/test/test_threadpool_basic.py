from pprint import pprint
import sys
import anfler.util.log.lw as lw
import anfler.mp.helper as mph

_log = lw.get_logger(__name__)

def local_method(payload):
    _log.info(f"Received {payload}")
    return "OK"


if __name__ == '__main__':
    lw.init_logging(level=lw.level.DEBUG)

    data =[
        ["anfler.xx.DummyClass@get_address", {
            "init_args": {"p1": 99, "p2": "p2_new value"},
            "args": "p2_args"}
         ],
        ["method", {
            "init_args": {},
            "args": {}}
         ],
        ["anfler.mp.dummy.dummyclass.DummyClass@echo", {
            "init_args": {},
            "args": {}}
         ],
        ["anfler.mp.dummy.dummyclass.DummyClass@echo", {
            "init_args": {"arg1": "P1", "arg2": "P2"},
            "method_args": {"data": 99}}
         ],
        ["anfler.mp.dummy.dummyclass.DummyClass@sleep", {
            "init_args": {},
            "method_args": {}}
         ],
        ["anfler.mp.dummy.dummyclass.DummyClass@sleep", {
            "init_args": {},
            "method_args": {"sleep_time":30}}
         ],
        ["anfler.anfler_afip.anfler_constancia_inscripcion.Constancia@get_address",
          {"init_args": None, "args": None}]
    ]
    for d in data[2:-1]:
        res=None
        try:
            _log.info("--------------------------------------------------------")
            res = mph.execute_class_method(d[0], **d[1])
            _log.info(res)
        except Exception as e:
            _log.error(f"{res}. {str(e)}")
