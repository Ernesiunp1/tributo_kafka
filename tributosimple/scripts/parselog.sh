#!/usr/bin/env bash
# ---------------------------------------------------------------------------
#
#
# ---------------------------------------------------------------------------
SCRIPT_NAME="parselog.sh"
SCRIPT_DATE="2010-11-30"
SCRIPT_DESC="Parser log script"


log_file=${1-tributosimple.log}
grep "Response from Job=" ${log_file} | egrep "INFO|ERROR"  |awk -F"|" 'BEGIN{OFS="|"}{print $5,$3,$13,$6,$7,$9,substr($10,0,40)}' | sed -e 's/"/\\"/g;s/'\''/"/g' |grep -v "^$"

#grep "Response from Job=" ${log_file} | egrep "INFO"  |awk -F"|" 'BEGIN{OFS="|"}{print $5,$3,$6,$7,$9}' | sed -e 's/"/\\"/g;s/'\''/"/g' |grep -v "^$"
#grep "Response from Job=" ${log_file} | egrep "ERROR" |awk -F"|" 'BEGIN{OFS="|"}{print $5,$3,$6,$7,$9}' | sed -e 's/"/\\"/g;s/'\''/"/g' |grep -v "^$"

