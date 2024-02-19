#!/usr/bin/env bash
# ---------------------------------------------------------------------------
#
#
# ---------------------------------------------------------------------------
SCRIPT_NAME="drops_jobs.sh"
SCRIPT_DATE="2021-01-12"
SCRIPT_DESC="Helper script"


service=${1-}
container=${2-anfler.db}

case $service in
afip) table=jobs_afip;;
arba) table=jobs_arba;;
agip) table=jobs_agip;;
admin) table=jobs_admin;;
*) echo "
Ops, missing tablename, valid  values: afip|arba|agip|admin
"
  exit
  ;;
esac



docker exec -it ${container} mysql -uroot -ppassw0rd mysql -e "delete from anflerdb.${table};commit;"
