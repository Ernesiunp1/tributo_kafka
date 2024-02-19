import sys
import os
import anfler.util.log.lw as lw

_log = lw.get_logger("anfler.app")
_log2 = lw.get_logger("anfler.app.2")
#---------------------------------------------------------------------------

if __name__ == '__main__':

    if len(sys.argv)>1:
        lw.init_logging(config_file=sys.argv[1])
    else:
        lw.init_logging(config_file="logging.json")

    _log.info("Info message...")
    _log.debug("Debug message...")

    _log2.info("Info2 message...")
    _log2.debug("Debug2 message...")

    lw.end_logging()