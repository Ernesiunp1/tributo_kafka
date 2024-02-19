#!/usr/bin/env bash
# ---------------------------------------------------------------------------
#
#
# ---------------------------------------------------------------------------
SCRIPT_NAME="tributosimple.sh"
SCRIPT_DATE="2010-11-26"
SCRIPT_DESC="Wrapper script"

# Get absoluth path
_file=`realpath $0`
_path=`dirname $_file`

# Set env
[ "${PYTHON}" == "" ] && PYTHON=python3
[ "${APP_BASE}" == "" ] && APP_BASE=/app

# ---------------------------------------------------------------------------
usage(){
  echo "
${SCRIPT_NAME} - (${SCRIPT_DATE})

 ${SCRIPT_DESC}

Usage:
  ${SCRIPT_NAME} start|stop|status [out]

Current Environment (from env.sh):
   APP_BASE=${APP_BASE}
   APP_CONFIG=${APP_CONFIG}
   APP_CONFIG_LOG=${APP_CONFIG_LOG}

   "
   exit
}

#---------------------------------------------------------------------------
getpid(){
  _app=${1-app.tributosimple}
  pid=`ps -ef|grep ${_app}|grep -v grep|awk '{print $2}'`
  if [ "$pid" = "" ]
  then
    echo ""
  fi
  echo $pid
}

#---------------------------------------------------------------------------

# Get absoluth path to script
_file=`realpath $0`
_path=`dirname $_file`


#
#
cd ${APP_HOME}
echo "Python is `${PYTHON} -V` (`which ${PYTHON}`)"


#
#
cmd=$1
out=$2

case $cmd in
start)
  echo "Starting app 'app.tributosimple' from '$PWD'"
  if [ "$out" = "" ]
  then
    nohup ${PYTHON} -m app.tributosimple -c ${APP_BASE}/etc/config.json -l ${APP_BASE}/etc/logging.json > ${APP_LOG}/nohup.out &
  else
    ${PYTHON} -m app.tributosimple -c ${APP_BASE}/etc/config.json -l ${APP_BASE}/etc/logging.json
  fi

  ;;
stop)
  pid=`getpid`
  [ "$pid" = "" ] && echo "App app.tributosimple is not running" && exit 1
  echo "Stoping app 'app.tributosimple' pid=$pid"
  kill -TERM $pid
  ;;
status)
  pid=`getpid`
  [ "$pid" = "" ] && echo "App app.tributosimple is not running" && exit 1
  echo "Status app 'app.tributosimple' pid=$pid"
  ps -To pcpu,user,ppid,pid,tid,etime,pmem,state,cmd -a | grep  app.tributosimple | grep -v grep

  ;;
*)
  usage
  ;;
esac


