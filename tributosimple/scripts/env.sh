#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Environment configuration
# Permission: 664 , 644, 600
# Usage: source ./env.sh
# ---------------------------------------------------------------------------


export PYTHON=python3
#
# Root path
if [ "${APP_BASE}" = "" ]
then
  export APP_BASE=/app
fi



# Application name (folder containing app script)
# Application script
export APP_NAME=tributosimple
export APP_SCRIPT_NAME=tributosimple.py

# Application Home
export APP_HOME=${APP_BASE}/${APP_NAME}
# Selenium driver
export APP_DRIVER=$APP_BASE/driver

# Config folder
export APP_ETC=${APP_BASE}/etc

# Log folder
export APP_LOG=${APP_HOME}/log

# Selenium driver
export APP_DRIVER=${APP_HOME}/driver

# Full app script
export APP_SCRIPT=${APP_HOME}/app/${APP_SCRIPT_NAME}

# Logging configuration
export APP_CONFIG_LOG=${APP_HOME}/etc/logging.json

# Application configuration files
export APP_CONFIG_FILE=${APP_HOME}/etc/config.json


# Modules
export PYTHONPATH="${APP_BASE}/${APP_NAME}:\
${APP_BASE}/utils:\
${APP_BASE}/kafka:\
${APP_BASE}/threadpool:\
${APP_BASE}/db:\
${APP_BASE}/webscrap"


export APP_CONFIG_JSON=`cat ${APP_CONFIG_FILE}`



#---------------------------------------------------------------------------
#
#---------------------------------------------------------------------------
getpid(){
  _app=${1-${APP_SCRIPT}}
  pid=`ps -ef|grep ${_app}|grep -v grep|awk '{print $2}'`
  if [ "$pid" = "" ]
  then
    echo ""
  fi
  echo $pid
}
