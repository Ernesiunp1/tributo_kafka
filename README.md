# Aplicacion Tributo Simple (Backend) 

---

Application include 5 images (see [docker-compose.yml](docker-compose.yml))
- anfler-app: Application image
- anfler-api: Application (API) image
- anfler-db: Myql image (service "db")
- bitnami/zookeeper: Kafka Zookeper (service "zookeeper1")
- bitnami/kafka: Kafka Zookeper (service "kafka1")


By default MySQL db is configured with the scripts defined in https://gitlab.anfler.com.ar:9999/tributosimple/kafka/tributosimple/-/tree/master/scripts/db


User, password, hostname and ports in [docker-compose.yml](docker-compose.yml) must be configured in application configuration file **config.json**, see
- https://gitlab.anfler.com.ar:9999/tributosimple/kafka/tributosimple/-/blob/master/README.md
- https://gitlab.anfler.com.ar:9999/tributosimple/kafka/api/-/blob/master/README.md


## Installation


1. Create application source folder

```
mkdir /docker/tributo_kafka/
```

2. Clone/Pull Devops sources

```
cd /docker/tributo_kafka/
git clone https://gitlab.anfler.com.ar:9999/pingino/tributo-docker.git .
```

3. Clone/Pull Application sources

```
cd /docker/tributo_kafka/

# module anfler-utils
# git clone https://gitlab.anfler.com.ar:9999/tributosimple/kafka/utils.git
git clone git@gitlab.anfler.com.ar:tributosimple/kafka/utils.git

# module anfler-kafka
#git clone https://gitlab.anfler.com.ar:9999/tributosimple/kafka/kafka.git
git clone git@gitlab.anfler.com.ar:tributosimple/kafka/kafka.git

# module anfler-threadpool
# git clone https://gitlab.anfler.com.ar:9999/tributosimple/kafka/threadpool.git
git clone git@gitlab.anfler.com.ar:tributosimple/kafka/threadpool.git

# module anfler-db 
# git clone https://gitlab.anfler.com.ar:9999/tributosimple/kafka/db.git
git clone git@gitlab.anfler.com.ar:tributosimple/kafka/db.git


# module anfler-scrapping
# git clone https://gitlab.anfler.com.ar:9999/tributosimple/pyapi.git
git clone git@gitlab.anfler.com.ar:tributosimple/pyapi.git

# application (backend)
# git clone https://gitlab.anfler.com.ar:9999/tributosimple/kafka/tributosimple.git
git clone git@gitlab.anfler.com.ar:tributosimple/kafka/tributosimple.git

# application (api)
# git clone https://gitlab.anfler.com.ar:9999/tributosimple/kafka/api.git
git clone git@gitlab.anfler.com.ar:tributosimple/kafka/api.git

```


4. Build application image

```
cd /docker/tributo_kafka/
mkdir -p tmp/app-logs
mkdir -p tmp/api-logs

docker-compose build 
```

Listing images:
```
docker image ls | egrep "anfler-|bitnami"

anfler-api                                      latest              17760d9e80ba        14 hours ago        1.07GB
anfler-app                                      latest              27ce80a593d4        6 days ago          919MB
anfler-db                                       latest              3277a356b0e5        5 days ago          711MB
bitnami/zookeeper                               latest              4d60135d7e29        3 weeks ago         467MB
bitnami/kafka                                   latest              3656120fdc8b        3 weeks ago         578MB

```



Start 
```
cd /docker/tributo_kafka/
docker-compose up

```

#### 5- Test application (Backend)

Go to **anfler.app** container
```
docker exec -it anfler.app bash
```
Send some messages
```
cd scripts
python send_message.py -n 2 -f msg-admin-*

2021-01-19 13:46:05.311 INFO database - __init__: Connected to root@anfler.db/anflerdb
2021-01-19 13:46:05.312 INFO send_message - load_json: Reading msg-admin-echo.json
2021-01-19 13:46:05.312 INFO send_message - load_json: Reading msg-admin-error.json
2021-01-19 13:46:05.371 INFO send_message - <module>: #01 Sent id=d90e6548-cd72-4e5e-a8db-870c64bc5410 entity/service=admin/echo {'offset': 0, 'topic': 'tributosimple-topic-admin', 'partition': 0, 'timestamp': 1611063965357}
2021-01-19 13:46:05.413 INFO send_message - <module>: #02 Sent id=e219c134-fb3d-4e6f-9b93-0cbc30ea546d entity/service=admin/error {'offset': 1, 'topic': 'tributosimple-topic-admin', 'partition': 0, 'timestamp': 1611063965410}
2021-01-19 13:46:05.413 INFO send_message - <module>: Sent 2 messages


```

Check application log 
```
cd /docker/tributo_kafka
tail tmp/app-logs/tributosimple.log

2021-01-19 13:46:05.374 INFO 139997283157760 anfler_main tributosimple - main: Batch 0_0 messages=1 pending_messages=0 pending_jobs=0
2021-01-19 13:46:05.375 INFO 139997244589824 anfler_0 dummy_service - echo: Received {}
2021-01-19 13:46:05.376 INFO 139997283157760 anfler_main tributosimple - main: Response from Job=5c188740-499c-460b-9469-89fd19855080|batch=0_0|offset=0||d90e6548-cd72-4e5e-a8db-870c64bc5410|echo|app.dummy_service.DummyService@echo|anfler|0|[]|{'key': None, 'service': 'echo', 'fn': 'app.dummy_service.DummyService@echo', 'entity': 'admin', 'user': 'anfler', 'auth': {'type': 'basic'}, 'offset': 0, 'partition': 0, 'wrap_in': 'message'}||partition=p0
2021-01-19 13:46:05.444 INFO 139997283157760 anfler_main tributosimple - main: Batch 1_1 messages=1 pending_messages=0 pending_jobs=0
2021-01-19 13:46:05.445 INFO 139997244589824 anfler_0 dummy_service - error: Received {}
2021-01-19 13:46:05.446 ERROR 139997283157760 anfler_main tributosimple - main: Response from Job=0e9f5f73-eb02-499f-8980-1506544f5f01|batch=1_1|offset=1||e219c134-fb3d-4e6f-9b93-0cbc30ea546d|error|app.dummy_service.DummyService@error|anfler|99|['Some error 1', 'Some error 2']|{'key': None, 'service': 'error', 'fn': 'app.dummy_service.DummyService@error', 'entity': 'admin', 'user': 'anfler', 'auth': {'type': 'basic'}, 'offset': 1, 'partition': 0, 'wrap_in': 'message'}||partition=p0

```
Check database records
```
docker exec -it anfler.db mysql -uroot -ppassw0rd mysql -e ' select id,msg_id,service,state,status,kafka_offset,kafka_partition from anflerdb.jobs_admin;'
mysql: [Warning] Using a password on the command line interface can be insecure.
+----+--------------------------------------+---------+-------+--------+--------------+-----------------+
| id | msg_id                               | service | state | status | kafka_offset | kafka_partition |
+----+--------------------------------------+---------+-------+--------+--------------+-----------------+
|  1 | d90e6548-cd72-4e5e-a8db-870c64bc5410 | echo    |     1 |      0 |            0 |               0 |
|  2 | e219c134-fb3d-4e6f-9b93-0cbc30ea546d | error   |     1 |     99 |            1 |               0 |
+----+--------------------------------------+---------+-------+--------+--------------+-----------------+

```
#### 6- Test application (API)

Execute:
```
curl -X POST 'http://anfler.api:80/jobs/admin/echo' \
--user 'anfler:passw0rd'
--header 'Authorization: Basic YW5mbGVyOnBhc3N3MHJk' \
--header 'Content-Type: application/json' \
--data-raw '{
  "header": {
    "auth": {
        "cuit": 20956804354, 
        "type": "basic", 
        "codif": 0, 
        "password": "CIv16953524b"
    }
  },
  "payload": {"message": "dummy data"}
}'
```
Output show be like:
``` 
{
  "id": "08835dda-d977-4785-94bf-01e13e9a945b",
  "entity": "admin",
  "service": "echo",
  "state": 0,
  "header": {
    "auth": {
      "cuit": 20956804354,
      "password": "CIv16953524b",
      "codif": 0,
      "type": "basic"
    }
  },
  "payload": {
    "message": "dummy data"
  },
  "status": 0,
  "errors": null
}

```

Also check id in DB record:
```
docker exec -it anfler.db mysql -uroot -ppassw0rd mysql -e ' select id,msg_id,service,state,status,kafka_offset,kafka_partition from anflerdb.jobs_admin;'

mysql: [Warning] Using a password on the command line interface can be insecure.
+----+--------------------------------------+---------+-------+--------+--------------+-----------------+
| id | msg_id                               | service | state | status | kafka_offset | kafka_partition |
+----+--------------------------------------+---------+-------+--------+--------------+-----------------+
|  1 | 0f7dc880-e222-481b-82a8-f92d5e451a29 | echo    |     1 |      0 |            1 |               0 |
|  2 | 92b230c4-22fd-4a88-a35c-95df79933201 | error   |     1 |     99 |            2 |               0 |
|  3 | fd85c367-ed8a-452f-83fb-05124ed99052 | error   |     1 |     99 |            3 |               0 |
|  4 | 2656304f-104c-4a82-b4fc-e9ed7d675884 | error   |     1 |     99 |            4 |               0 |
|  5 | ac0cf90f-4bf6-4231-988d-3e4e2b0902d5 | echo    |     1 |      0 |            5 |               0 |
|  6 | ae23177b-f69c-43cf-bf40-3fc6c1c44cf2 | echo    |     0 |      0 |           -1 |              -1 |
|  7 | 08835dda-d977-4785-94bf-01e13e9a945b | echo    |     0 |      0 |           -1 |              -1 | <<<< THIS
+----+--------------------------------------+---------+-------+--------+--------------+-----------------+

