#!/usr/bin/env bash
# ---------------------------------------------------------------------------
#
#
# ---------------------------------------------------------------------------

# Get absoluth path to script
_file=`realpath $0`
_path=`dirname $_file`

# Set env
. "$_path/env.sh"


#
#
_num_message=${1-1}
_use_db=${2-YES}

cd $APP_HOME/scripts > /dev/null 2>&1

python $APP_HOME/scripts/send_message.py $@

cd - > /dev/null 2>&1