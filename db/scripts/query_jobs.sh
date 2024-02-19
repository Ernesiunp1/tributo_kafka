#!/usr/bin/env bash
# ---------------------------------------------------------------------------
#
#
# ---------------------------------------------------------------------------
SCRIPT_NAME="query_jobs.sh"
SCRIPT_DATE="2021-01-12"
SCRIPT_DESC="Helper script"


service=${1-}
container=${2-anfler.db}

case $service in
afip|arba|agip|admin)
  sql=`cat query_jobs.sql |sed "s/anflerdb.jobs/anflerdb.jobs_${service}/g"`
  ;;
services)
  sql=`cat query_jobs_services.sql`
  ;;
*) echo "
Ops, missing tablename, valid  values: afip|arba|agip|admin|services
"
  exit
  ;;
esac
#
docker exec -it ${container} mysql -uroot -ppassw0rd mysql -e "${sql}"
