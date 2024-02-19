import anfler.util.config.cfg as cfg
import anfler.util.msg.message as msg
import anfler.util.log.lw as lw
import anfler.kafka_wrapper.kw as kw

import time
import random
from datetime import datetime


_log = lw.get_logger("anfler.kafka")


if __name__ == '__main__':
    lw.init_logging()
    lw.set_logger_level("anfler.kafka",lw.level.INFO)
    cfg.load("config_testing.json")
    kp = kw.KafkaProducerWrapper(cfg.get("kafka"))

    while True:
        data = msg.get_basic_message(payload={"data": str(datetime.now()),"i": random.randint(0,10)})
        kp.send(cfg.get("kafka.producer_topics")[0],data)
        _log.info(f"Message sent {data}")
        time.sleep(10)
    kp.close()
    lw.end_logging()