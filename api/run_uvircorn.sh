#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Wrapper script to start Tributosimple application (API)
#
# ---------------------------------------------------------------------------
SCRIPT_NAME="run_uvicorn.sh"
SCRIPT_DATE="2021-02-22"
SCRIPT_DESC="Wrapper script to start Tributosimple application (API)"



#
# Export the following variables before run the script and install all dependencies
# Note that env variables are already defined in file Dockerfile.api
#
export APP_HOME="${APP_HOME:-/api}"
export APP_LOG="${APP_LOG:-${APP_HOME}/logs}"
export APP_CONFIG_FILE="${APP_CONFIG_FILE:-${APP_HOME}/etc/config.json}"
export APP_CONFIG_LOG_FILE="${APP_CONFIG_LOG_FILE:-${APP_HOME}/etc/logging.json}"

#
export PYTHONPATH="${APP_HOME}:${PYTHONPATH}"
uvicorn --host ${APP_HOST:="0.0.0.0"} --port ${APP_PORT:=80} ${APP_ACCESS_LOG} ${APP_RELOAD} --lifespan ${APP_LIFESPAN:=on} "app.anfler_api:app"
 