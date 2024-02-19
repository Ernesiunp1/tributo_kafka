import anfler.util.config.cfg as cfg
import anfler.util.msg.message as msg
import anfler.util.log.lw as lw
import anfler.kafka_wrapper.kw as kw


_log = lw.get_logger("anfler.kafka")

def processMessage(m):
    if m["payload"]["i"] > 5:
        return 1
    else:
        return 0


if __name__ == '__main__':
    lw.init_logging()
    lw.set_logger_level("anfler.kafka",lw.level.DEBUG)
    cfg.load("config_testing.json")
    kc = kw.KafkaConsumerWrapper(cfg.get("kafka"))
    # while True:
    #     records = kw.poll()
    #     kw.print_records(records)
    #     kw.print_messages(kw._buildMessages(records))

    while True:
        batch = kc.poll()
        kc.print_messages(batch)
        if len(batch["messages"]) > 0 :
            if batch["ok"] == False:
                # Invalid messages received
                _log.warning(f"Batch {batch['id']} failed, comitting")
                kc.commit()
            else:
                acc=0
                for i,m in enumerate(batch["messages"]):
                    _log.info(f"Processing message {str(m)}")
                    rc = processMessage(m)
                    _log.info(f"Msg#{i} rc={rc}")
                    acc+=rc
                if acc > 0:
                    _log.info(f"Messages processed failed {acc}")
                else:
                    _log.info(f"Messages processed OK {acc}")
                kc.commit()
    kc.close()
    lw.end_logging()