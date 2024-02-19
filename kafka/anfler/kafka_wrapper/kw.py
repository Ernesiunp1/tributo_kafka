"""Kafka wrapper
"""



import copy
import json
import uuid
import sys
import time

import anfler.util.log.lw as lw
import anfler.util.msg.message as msg
from anfler.util.helper import mask_data

from kafka import KafkaConsumer, KafkaProducer



_log = lw.get_logger("anfler.kafka")
_logp = lw.get_logger("anfler.kafka.producer")
_logc = lw.get_logger("anfler.kafka.consumer")
# ---------------------------------------------------------------------------
#   Kafka
# ---------------------------------------------------------------------------
NULL_BATCH_ID = "-1_-1"
BATCH = {
    "id": NULL_BATCH_ID,
    "ok": True,
    "messages": []
}


# ---------------------------------------------------------------------------
#   Base class
# ---------------------------------------------------------------------------
class KafkaWrapper():
    __DEFAULT_INIT_RETRY__ = 10
    __DEFAULT_INIT_RETRY_DELAY__ = 60
    def __init__(self,config):
        self._config = config
        if "consumer" in config:
            self._expand_config(config["consumer"])
        if "producer" in config:
            self._expand_config(config["producer"])
        self._init_retry_count = 0
        self._init_retry_max = self._config.get("init_retry_max", KafkaWrapper.__DEFAULT_INIT_RETRY__)
        self._init_retry_delay = self._config.get("init_retry_delay", KafkaWrapper.__DEFAULT_INIT_RETRY__)

    def _expand_config(self, config):
        for k, v in config.items():
            if isinstance(v, str):
                try:
                    if callable(eval(v)):
                        config[k] = eval(v)
                except NameError as e:
                    pass

    def print_records(self, records):
        if len(records) == 0:
            _log.debug("No records...")
            return
        for p, records in records.items():
            for i, record in enumerate(records):
                _log.info(f"{i:02} p{record.partition} offset={record.offset:05} data={str(record.value.decode('utf-8'))}")

    def print_messages(self, batch, include_payload=True):
        if len(batch["messages"]) == 0:
            _log.debug("No messages...")
            return
        _log.debug(f"Batch {batch['id']} ok={batch['ok']} len={len(batch['messages'])}")
        for i, m in enumerate(batch["messages"]):
            if include_payload:
                _log.debug(f"{i:02} {mask_data(m)}")
            else:
                _log.debug(f"{i:02} {mask_data(m)}")

    def close(self,autocommit=False):
        if hasattr(self,"_consumer"):
            self._consumer.close(autocommit=autocommit)
            _log.info(f"Consumer closed, closed={self._consumer._closed}")
        if hasattr(self,"_producer"):
            self._producer.close()
            _log.info(f"Producer closed, closed={self._producer._closed}")

    def get_metrics(self):
        metrics = []
        if self._producer:
            metrics.append(self._producer.metrics())
        if self._consumer:
            metrics.append(self._consumer.metrics())
        return metrics

    def init(self, config,  type="consumer"):
        while self._init_retry_count < self._init_retry_max:
            try:
                if type == "consumer":
                    kafka_object = KafkaConsumer(**config)
                else:
                    kafka_object = KafkaProducer(**config)
                return kafka_object
            except Exception as e:
                _logc.error(f"Error initilializing {type}, attempt #{self._init_retry_count} of {self._init_retry_max}, sleeping {self._init_retry_delay} secs",exc_info=True)
                time.sleep(self._init_retry_delay)
                self._init_retry_count += 1

    def is_bootstrap_connected(self):
        pass
# ---------------------------------------------------------------------------
#   Consumer wrapper
# ---------------------------------------------------------------------------
class KafkaConsumerWrapper(KafkaWrapper):
    def __init__(self, config, debug=False):
        super(KafkaConsumerWrapper, self).__init__(config)
        self._consumer = None
        self._paused = False
        if debug == True or self._config["debug"] == True:
            lw.get_logger("anfler.kafka.consumer").setLevel(lw.level.DEBUG)

        _logc.debug(f"Starting Kafka consumer, config={config}")
        assert "consumer" in config, "Configuration  doesn't have a consumer section. Aborting"
        self._consumer = self.init(self._config["consumer"], "consumer")
        if not self._consumer:
            raise Exception("Cannot connect to Kafka after {self._init_retry_max} attempts" )

        self._subscribe()
        _logc.info(f"Subscribed to {self._config['consumer_topics']}, max_poll_records={self._config['consumer']['max_poll_records']} consumer_timeout_ms={self._config['consumer']['consumer_timeout_ms']}")

    def is_bootstrap_connected(self):
        return self._consumer.bootstrap_connected()

    def _subscribe(self):
        # for t in self._config["consumer_topics"]:
        #     print(t)
        self._consumer.subscribe(self._config["consumer_topics"])

    def poll(self, timeout_ms=5000):
        """Wrapper for KafkaConsumer.poll()

        Seee https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html

        Arguments:
            timeout_msk: poll timeout, default=5000
        Returns:
            array of dict BASIC_MESSAGE
        """
        records = {}
        #records = self._consumer.poll(timeout_ms=timeout_ms)
        if self._paused == False:
            records = self._consumer.poll(timeout_ms=timeout_ms)
        else:
            time.sleep(timeout_ms/1000)
        # try:
        #     records =  self._consumer.poll(timeout_ms=timeout_ms)
        # except Exception as e:
        #     print(e)
        #     _log.error(f"Error during poll {str(e)}",stack_info=True)
        return self._buildMessages(records)


    def commit(self, offset=-1):
        """Commit against Kafka
        See https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html#kafka.KafkaConsumer.commit
        """
        _logc.debug(f"Commiting")
        self._consumer.commit()

    def pause(self):
        if self._paused == False:
            self._consumer.pause()
            self._paused = True

    def resume(self):
        if self._paused == True:
            self._consumer.resume()
            self._paused = False

    def _getBatchId(self, messages):
        """Build an id to identify a batch of messages.
        A batch of messages is built using _buildMessages()

        Args:
        :param messages: array of messages returned by _buildMessages()
        :returns A batch Id with following format:
        <first_offset from array mesages>_<last_offset from array messages>
        If -1_-1 if array is empty

        Example: 1923_1927 (for an array with 5 messages)
        """
        if len(messages) != 0:
            return "{0}_{1}".format((messages[0])["header"]["offset"],
                                    (messages[len(messages) - 1])["header"]["offset"])
        else:
            return NULL_BATCH_ID


    def _buildMessages(self, records):
        batch = copy.deepcopy(BATCH)
        messages = []
        i = 0
        batch_ok = True
        for p, records in records.items():
            for i, record in enumerate(records):
                message = msg.get_basic_message(header={"offset": -1, "partition": -1})
                try:
                    header ={"offset":record.offset, "partition": record.partition, "key": record.key}
                    message = msg.update_message(message,header=header)
                    # jsondata = json.loads(record.value.decode('utf-8'))
                    jsondata = record.value
                    message = msg.update_message(message, id=jsondata.get("id"), header=jsondata.get("header"),payload=jsondata.get("payload"))
                    message = msg.update_message(message,header=header)
                    messages.append(message)
                except KeyError as ke:
                    _logc.error(f"Invalid message for offset '{record.offset}', missing key {ke}. <{str(record)}>")
                    batch_ok = False
                    messages.append(message)
                except NameError as ne:
                    _logc.error(f"Invalid message for offset '{record.offset}'. <{str(record)}>")
                    batch_ok = False
                    messages.append(message)
                except json.JSONDecodeError as je:
                    _logc.error(f"Invalid message format received, expecting JSON. <{str(record)}>")
                    batch_ok = False
                    messages.append(message)
                except Exception as e:
                    _logc.error(f"Error reading message from Kafka. <{str(record)}> ({str(e)})")
                    batch_ok = False
                    messages.append(message)
                _log.debug(f"Message received {mask_data(message)}")
        batch["id"] = self._getBatchId(messages)
        batch["ok"] = batch_ok
        batch["messages"] = messages

        return batch


# ---------------------------------------------------------------------------
#   Producer wrapper
# ---------------------------------------------------------------------------
class KafkaProducerWrapper(KafkaWrapper):
    def __init__(self, config, debug=False):
        super(KafkaProducerWrapper, self).__init__(config)
        self._producer = None
        if debug == True or self._config["debug"] == True:
            lw.get_logger("anfler.kafka.producer").setLevel(lw.level.DEBUG)

        _logp.debug(f"Starting Kafka producer, config={config}")
        assert "producer" in config, "Configuration  doesn't have a producer section. Aborting"

        #self._producer = KafkaProducer(**self._config["producer"])
        self._producer = self.init(self._config["producer"], "producer")
        if not self._producer:
            raise Exception(f"Cannot connect to Kafka after {self._init_retry_max} attempts" )
        _logp.debug(f"New producer")

    def is_bootstrap_connected(self):
        return self._producer.bootstrap_connected()

    def send(self, topic, message):
        """Send a messages to Kafka

        :param topic: topic nam
        :param message: message to sent
        :return: Dict
        {
            "offset": <offsetZ,
            "topic": <topic name>,
            "partition": <topic partition>,
            "timestamp": <message timestamp>
        }
        """
        _log.debug(f"Sending to topic {topic}  message={message}")
        f = self._producer.send(topic, value=message)
        self._producer.flush()
        return {
            "offset": f.value.offset,
            "topic": f.value.topic,
            "partition": f.value.topic_partition.partition,
            "timestamp": f.value.timestamp
        }


