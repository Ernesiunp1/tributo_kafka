#!/usr/bin/env bash
# ---------------------------------------------------------------------------
#
#
# ---------------------------------------------------------------------------
SCRIPT_NAME="kafka_admin.sh"
SCRIPT_DATE="2010-11-26"
SCRIPT_DESC="Kafka admin wrapper script"


# Get absoluth path
_file=`realpath $0`
_path=`dirname $_file`

# Set env
. "$_path/env.sh" >/dev/null 2>&1
# Default values:
if [ "KAFKA_TOPIC" = "" ]; then
  KAFKA_TOPIC=tributosimple-topic-admin
fi

if [ "$KAFKA_GROUP" = "" ]; then
  KAFKA_GROUP=tributo-app
fi

if [ "$KAFKA_GROUP" = "" ]; then
  KAFKA_GROUP=tributo-app
fi

if [ "$KAFKA_BOOTSTRAP" = "" ]; then
  KAFKA_BOOTSTRAP=anfler.kafka:9092
fi

if [ "$KAFKA_ZOOKEEPER" = "" ]; then
  KAFKA_ZOOKEEPER=anfler.kafka:2181
fi

if [ "$KAFKA_HOME" == "" ]; then
  echo -e "\nVariable KAFKA_HOME not defined. Please export KAFKA_HOME=<Kafka installation folder>\n"
  exit 1
fi

echo "========================================="
echo "KAFKA_HOME=$KAFKA_HOME"
echo "Kafka version=`$KAFKA_HOME/bin/kafka-topics.sh --version`"
echo "========================================="

_cmd=${2}
_obj=${1-all}
_kgroup=${3-$KAFKA_GROUP}
_ktopic=${4-$KAFKA_TOPIC}
_offset=${5-0}
_bootstrap=${KAFKA_BOOTSTRAP}
_zookeeper=${KAFKA_ZOOKEEPER}

_reset_topic=${3-$KAFKA_TOPIC}
_reset_offset=${4-0}
_reset_partitions=${5-0}

_create_topic=${3-$KAFKA_TOPIC}
_create_topic_partitions=${4-1}

_delete_topic=${3-$KAFKA_TOPIC}
_delete_topic_partitions=${4-0}
_describe_topic=${3-$KAFKA_TOPIC}

# 30 minutes
RETENTION_MS_DEFAULT=1800000
#---------------------------------------------------------------------------
usage(){
  echo "
$SCRIPT_NAME

Usage
  - List topics and consumers
    ${SCRIPT_NAME} all|topic|consumer list

  - Create topic (default: partitions=1 retention.ms=${RETENTION_MS_DEFAULT})
    ${SCRIPT_NAME} topic create <topic> [partitions (default 1)]

  - Delete messages from topic
    ${SCRIPT_NAME} topic purge <topic> <to_offset> <partitions comma separated>

  - Delete topic
    ${SCRIPT_NAME} topic delete <topic>

  - Describe consumers
    ${SCRIPT_NAME} consumer list

  - Delete consumer
    ${SCRIPT_NAME} consumer delete <group>

  - Reset offser to consumer group
    ${SCRIPT_NAME} consumer reset <group> <topic> [offset (default 0)]
"
exit
}
check_args(){
case $1 in
  all|ps|k) ;;
  *) usage;;
esac

}
#---------------------------------------------------------------------------
k_consumer_describe(){
  # /sw/apache/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --offsets  --group tributo-app
  # /sw/apache/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe   --group tributo-app  --members --all-topics
  ${KAFKA_HOME}/bin/kafka-consumer-groups.sh --bootstrap-server ${_bootstrap} --describe --offsets --group ${1}
}

#---------------------------------------------------------------------------
k_consumer_reset(){
  # /sw/apache/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --offsets  --group tributo-app
  # /sw/apache/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe   --group tributo-app  --members --all-topics
  if [ "$3" == "--to-earliest" ]
  then
    opts="--all-topics"
  elif  [ "$3" == "--to-latest" ]
  then
    opts="--to-latest"
  else
    opts="--to-offset $3"
  fi

  ${KAFKA_HOME}/bin/kafka-consumer-groups.sh --bootstrap-server ${_bootstrap} --reset-offsets --execute --group ${1} --topic ${2} ${opts}
}
#---------------------------------------------------------------------------
k_consumer_list(){
  ${KAFKA_HOME}/bin/kafka-consumer-groups.sh --bootstrap-server ${_bootstrap} --list
}
#---------------------------------------------------------------------------
k_consumer_delete(){
  ${KAFKA_HOME}/bin/kafka-consumer-groups.sh --bootstrap-server ${_bootstrap} --delete --group ${1}
}
#---------------------------------------------------------------------------
k_topic_list(){
  ${KAFKA_HOME}/bin/kafka-topics.sh  --zookeeper ${KAFKA_ZOOKEEPER}  --list
}
#---------------------------------------------------------------------------
k_topic_describe(){
  ${KAFKA_HOME}/bin/kafka-topics.sh  --zookeeper ${KAFKA_ZOOKEEPER}  --describe --topic $1
}
#---------------------------------------------------------------------------
k_topic_delete(){
  ${KAFKA_HOME}/bin/kafka-topics.sh  --zookeeper ${KAFKA_ZOOKEEPER}  --delete --topic $1
}
#---------------------------------------------------------------------------
write_out(){
  echo "$1" >> delete-records.json
}
k_topic_reset(){
  _topic=$1
  _offset=$2

  _aux=`echo "$3" | sed "s/,/ /g"`
  _partitions=(`echo ${_aux}`)

  ${KAFKA_HOME}/bin/kafka-configs.sh  --zookeeper ${KAFKA_ZOOKEEPER}  --alter --entity-type topics --entity-name ${_topic} --add-config retention.ms=1000
  echo "Setting retention time to ${RETENTION_MS_DEFAULT}"
  ${KAFKA_HOME}/bin/kafka-configs.sh  --zookeeper ${KAFKA_ZOOKEEPER}  --alter --entity-type topics --entity-name ${_topic} --add-config retention.ms=${RETENTION_MS_DEFAULT}
  return
  rm delete-records.json* 2>/dev/null
  write_out "{"
  write_out "\"partitions\": ["

  len=${#_partitions[@]}
  for (( i=0; i<$len; i++ ))
  do
    echo "$_topic, $_offset, ${_partitions[$i]}"
    write_out "{\"topic\":  \"$_topic\", \"partition\": ${_partitions[$i]}, \"offset\": $_offset},"
    # {
    #    "partitions": [
    #        {"topic": "test-topic", "partition": 0, "offset": 20}
    #    ],
    #    "version": 1
    #}
  done
  # Delete last comma
  sed -i.bak -e '$s/,$//' delete-records.json
  write_out "],"
  write_out "\"version\":1"
  write_out "}"
  ${KAFKA_HOME}/bin/kafka-delete-records.sh --bootstrap-server ${_bootstrap} --offset-json-file delete-records.json
}
#---------------------------------------------------------------------------
k_monitor(){
  echo -e "\n=== Groups"
  ${KAFKA_HOME}/bin/kafka-consumer-groups.sh --bootstrap-server ${_bootstrap} --list

  echo -e "\n=== Group ${KAFKA_GROUP}"
  #${KAFKA_HOME}/bin/kafka-consumer-groups.sh --bootstrap-server ${_bootstrap} --describe --group ${_kgroup}
  ${KAFKA_HOME}/bin/kafka-consumer-groups.sh --bootstrap-server ${_bootstrap} --describe --offsets --group ${_kgroup}
  #${KAFKA_HOME}/bin/kafka-consumer-groups.sh --bootstrap-server ${_bootstrap} --describe --members --group ${_kgroup} --state

  echo -e "\n=== Topics"
  ${KAFKA_HOME}/bin/kafka-topics.sh  --zookeeper ${KAFKA_ZOOKEEPER}  --describe --topic ${KAFKA_TOPIC}
}
#---------------------------------------------------------------------------
k_topic_create() {
  ${KAFKA_HOME}/bin/kafka-topics.sh  --zookeeper ${KAFKA_ZOOKEEPER} --create --topic ${1} --partitions ${2} --replication-factor 1 --config retention.ms=${RETENTION_MS_DEFAULT}
  ${KAFKA_HOME}/bin/kafka-topics.sh  --zookeeper ${KAFKA_ZOOKEEPER}  --describe --topic ${1}
}


#${KAFKA_HOME}/bin/kafka-configs.sh --zookeeper ${_zookeeper}  --alter --entity-type topics --entity-name ${_ktopic} --add-config retention.ms=1000
#${KAFKA_HOME}/bin/kafka-configs.sh --zookeeper ${_zookeeper}  --alter --entity-type topics --entity-name ${_ktopic} --add-config retention.ms=86400000
#${KAFKA_HOME}/bin/kafka-delete-records.sh --bootstrap-server ${_bootstrap} --offset-json-file delete-records.json

#---------------------------------------------------------------------------
#   Main
#---------------------------------------------------------------------------
[ $# -lt 2 ] && usage


case "${_obj}_${_cmd}" in
all_list)
    echo "=== Topics"
    k_topic_list
    echo "=== Consumers"
    k_consumer_list
    ;;
topic_list)
    echo "=== Topics"
    k_topic_list
    ;;
consumer_list)
    echo "=== Consumers"
    k_consumer_list
    ;;
topic_describe)
  echo "Describing topic ${_describe_topic}"
  k_topic_describe ${_describe_topic}
  ;;
topic_create)
  echo "=== Creating topic ${_create_topic} partitions=${_create_topic_partitions}"
  k_topic_create $_create_topic $_create_topic_partitions
  ;;
topic_delete)
  echo "=== Deleting topic ${_delete_topic}"
  k_topic_delete $_delete_topic $_delete_topic_partitions
  ;;
topic_purge)
  echo "=== Deleting records from topic ${_reset_topic} partitions=<${_reset_partitions}> from offset ${_reset_offset}"
  k_topic_reset ${_reset_topic} ${_reset_offset} ${_reset_partitions}
  ;;
consumer_describe)
  echo "=== Listing consumers groups: ${_kgroup}"
  k_consumer_describe ${_kgroup}
  ;;
consumer_delete)
  echo "=== Listing consumers groups: ${_kgroup}"
  k_consumer_delete ${_kgroup}
  ;;
consumer_reset)
  echo "=== Reseting offset to consumer group: ${_kgroup}"
  k_consumer_reset ${_kgroup}  ${_ktopic} ${_offset}
  ;;
*)
  usage
  ;;
esac


#while :
#do
#  echo "=========================================================================================="
#  if ([ "$_cmd" = "all" ] || [ "$_cmd" = "ps" ]); then
#    k_ps $_app 2>/dev/null
#  fi
#
#  if ([ "$_cmd" = "all" ] || [ "$_cmd" = "k" ]) ;then
#    k_monitor 2>/dev/null
#  fi
#  sleep 5
#  clear
#done
