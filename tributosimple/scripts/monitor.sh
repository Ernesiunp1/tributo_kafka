#!/usr/bin/env bash
# ---------------------------------------------------------------------------
#
#
# ---------------------------------------------------------------------------
SCRIPT_NAME="monitor.sh"
SCRIPT_DATE="2010-11-26"
SCRIPT_DESC="Monitoring script"


# Get absoluth path
_file=`realpath $0`
_path=`dirname $_file`

# Set env
. "$_path/env.sh"





_cmd=${1-all}
_app=${2-$APP_SCRIPT}
_kgroup=${3-$KAFKA_GROUP}
_ktopic=${4-$KAFKA_TOPIC}

_bootstrap=${KAFKA_BOOTSTRAP}
_zookeeper=${KAFKA_ZOOKEEPER}


#---------------------------------------------------------------------------
usage(){
  echo "
monitor.sh all|ps|k app
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
k_ps() {
  set -x
  _app=$1
  _pid=`getpid $_app`
  echo -e "\n=== Application $_app $_pid"
  [ "${_pid}" = "" ] && echo "App ${_app} is not running"; exit 1
  pstree -p $_pid
  ps -To pcpu,user,ppid,pid,tid,times,etimes,pmem,state,%cpu,cmd -a | grep  $_pid | grep -v grep

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
  ${KAFKA_HOME}/bin/kafka-topics.sh  --zookeeper ${KAFKA_ZOOKEEPER} --create --topic ${KAFKA_TOPIC} --partitions 1 --replication-factor 1
  ${KAFKA_HOME}/bin/kafka-topics.sh  --zookeeper ${KAFKA_ZOOKEEPER}  --describe --topic ${KAFKA_TOPIC}
  ${KAFKA_HOME}/bin/kafka-topics.sh  --zookeeper ${KAFKA_ZOOKEEPER}  --list
}


#${KAFKA_HOME}/bin/kafka-configs.sh --zookeeper ${_zookeeper}  --alter --entity-type topics --entity-name ${_ktopic} --add-config retention.ms=1000
#${KAFKA_HOME}/bin/kafka-configs.sh --zookeeper ${_zookeeper}  --alter --entity-type topics --entity-name ${_ktopic} --add-config retention.ms=86400000
#${KAFKA_HOME}/bin/kafka-delete-records.sh --bootstrap-server ${_bootstrap} --offset-json-file delete-records.json

#---------------------------------------------------------------------------
#   Main
#---------------------------------------------------------------------------
[ $# -lt 1 ] && usage
while :
do
  echo "=========================================================================================="
  if ([ "$_cmd" = "all" ] || [ "$_cmd" = "ps" ]); then
    k_ps $_app 2>/dev/null
  fi

  if ([ "$_cmd" = "all" ] || [ "$_cmd" = "k" ]) ;then
    k_monitor 2>/dev/null
  fi
  sleep 5
  clear
done
