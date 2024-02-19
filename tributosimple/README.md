# Aplicacion Tributo Simple (Backend) 

---

## Introduction
TributoSimple (backend) is a Python 3 application

The application consume  messages from kafka topics, for each message will execute a web-scrapping operation against some entity (afip, agip, arba) , then update the database (mysql) with the response from the entity.


## Application and modules 
Main application file is located in  [app/tributosimple.py](app/tributosimple.py). Source code:

- Application [tributosimple](https://gitlab.anfler.com.ar:9999/tributosimple/kafka/tributosimple.git)
- Module [anfler-utils](https://gitlab.anfler.com.ar:9999/tributosimple/kafka/utils.git)
- Module [anfler-threadpool](https://gitlab.anfler.com.ar:9999/tributosimple/kafka/threadpool.git)
- Module [anfler-kafka](https://gitlab.anfler.com.ar:9999/tributosimple/kafka/kafka.git)
  
  This module use [kafka-python](https://kafka-python.readthedocs.io/en/master/index.html) 
- Module [anfler-db](https://gitlab.anfler.com.ar:9999/tributosimple/kafka/db.git)
  
  This module use [SQLAlchemy](https://www.sqlalchemy.org/) and [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/) to access to MySQL
- Module [anfler-scrapping](https://gitlab.anfler.com.ar:9999/tributosimple/pyapi.git)
  
  This module use [selenium](https://www.selenium.dev/selenium/docs/api/py/index.html)



## Installation

Please refer to Devops repo: [README.md](https://gitlab.anfler.com.ar:9999/pingino/tributo-docker/-/blob/master/README.md)


## Configuration

### 1- Database

Application requires MySQL DB, driver used is **mysql-connector-python==8.0.22** (https://gitlab.anfler.com.ar:9999/tributosimple/kafka/db/-/blob/master/setup.py).


- Basic user access [user/password](scripts/db/0_db_user.sql)
  
  User and password configuration.
  
- Table [jobs_services](scripts/db/2_db_table_job_service.sql)
  
  Service definition (name and function to be executed) for each entity, use this file as a reference to populate this table.
  
- Tables [jobs_afip, jobs_agip, jobs_arba, jobs_admin](scripts/db/1_db_table_jobs.sql)
  
  Jobs execution log for each entity (afip, agip, arba), entity **admin** is used for testing/monitoring purpose 


### 2- Kafka
  For each entity a topic **tributosimple-topic-<entity>** must be created, for example **tributosimple-topic-afip** ([config.json: consumer_topics](#31-file-etcconfigjson) 
  
Depending of Kafka property [auto.create.topics.enable](https://kafka.apache.org/documentation/#brokerconfigs_auto.create.topics.enable) topic will be created automatically

### 3- Configuration files
Application is configured using the following files:
- [etc/config.json](etc/config.json)
  
  Configuration file
- [etc/logging.json](etc/logging.json)
  
   Logging configuration. Logging is implemented using **python logging package**: https://docs.python.org/3/library/logging.html. (This package is similar to Log4j)
  
- Scrapping
  
  TBD

#### 3.1 File etc/config.json
There are 4 sections to configure:
- kafka
  This section configure Kafka module (kafka client)
  ```
  "kafka": {
    "consumer": {
      "bootstrap_servers": ["anfler.kafka:9092"],
      "value_deserializer": "lambda x: json.loads(x)",
      "consumer_timeout_ms": 5000,
      "max_poll_records": 5,
      "enable_auto_commit": false,
      "auto_offset_reset": "earliest",
      "group_id": "tributo-app",
      "client_id": "tributo-client"
    },
    "consumer_topics": ["tributosimple-topic-admin", "tributosimple-topic-afip","tributosimple-topic-arba", "tributosimple-topic-agip"],
    "debug": false,
    "init_retry_max": 10,
    "init_retry_delay": 60
  },
  ```
  - **consumer** is documented in [Kafka Client](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html)
    
    Application will poll a maximun of **max_poll_records** records from topics every **consumer_timeout_ms**  milliseconds
  - **consumer_topics** List of topics to subscribe
  - **debug** enable debug on loggers "anfler.kafka", please use [etc/logging.json](etc/logging.json)
  - **init_retry_max** and **init_retry_delay** retry options used when application start, these values are used only when app is initializing, allowing to "wait" for Kafka server
  
- pool
  ```
   "pool": {
    "preffix": "anfler",
    "max_workers": 5,
    "wait_timeout_sec": 60,
    "monitor_interval_sec": 120,
    "monitor_timeout_sec": 90,
    "child_process_names": ["chrome", "chromedriver"]
  },
  ```
  - **preffix** thread preffix
  - **max_workers** max number of threads to run, this value should match **kafka.consumer.max_poll_records**
  - **wait_timeout_sec** pool will wait **wait_timeout_sec** for the execution of service (scrapping), after reach the timeout all chlds process defined in **child_process_names** are killed.
  - **monitor_interval_sec**, **monitor_timeout_sec** control monitor thread loop. 
    Monitor thread output allows to check any "zombie" threads and process, this thread will not execute any action on these threads/processes
  - **child_process_names** child process names to be killed when timeout is reached. 
- db
  ```
   "db": {
      "user": "anfleruser",
      "password": "passw0rd",
      "host": "anfler.db",
      "port": 3306,
      "database": "anflerdb",
      "init_retry_max": 10,
      "init_retry_delay": 10,
      "pool_recycle": 1800,
      "pool_size": 2
  }
  ```
  - **init_retry_max**, **init_retry_delay** retry options used when application start, these values are used only when app is initializing, allowing to "wait" for DB server
  - **user**, **password** database user and password
  - **host**, **port**, **database** hostname, port and database name
  - **pool_recycle**, **pool_size**, please refer to https://docs.sqlalchemy.org/en/14/core/engines.html#sqlalchemy.create_engine
  
- logging
  Please refer to https://docs.python.org/3/library/logging.config.html#logging.config.listen
  
#### 3.2 File etc/loggin.json
  This file contains all logger defined for the application, see https://docs.python.org/3/library/logging.config.html#module-logging.config

#### 3.3 Scrapping
  TBD


## Application build and installation

To install each module run on each project 
```
setup.py bdist_wheel 
cd dist
python install --force-reinstall anfler_*whl

```
To build docker image, please refer to Devops repo: [README.md](https://gitlab.anfler.com.ar:9999/pingino/tributo-docker/-/blob/master/README.md)

## Application start 

After installing all modules, run 
```
python3 -m app.tributosimple -c <path to config.json> -l <path to logging.json>
```

Or, run with script **<tributosimple path>/scripts/tributosimple.sh**:

```
# edit file <tributosimple path>/scripts/env.sh according to your environment:

<tributosimple path>/scripts/tributosimple.sh  start out
```



## Environment properties

- **APP_CONFIG_FILE**: allows to override arguments "-c",
- **KAFKA_CONFIG**: allows to override kafka section in config.json
- **DB_CONFIG**: allows to override db section in config.json
- **POOL_CONFIG**: allows to override kafka section in pool.json

For example, to override pool section:
```
# Extract current pool section
jq "{pool:.pool} " /app/tributosimple/etc/config.json > pool.json

# Update file pool.json   


# Start app  using pool.json file
export POOL_CONFIG=`cat pool.json` 
python3 -m app.tributosimple -c /app/tributosimple/etc/config.json  -l /app/tributosimple/etc/logging.json

```

## Development setup

### 1- Define a conda environment:
```
conda create  --yes --name anfler python=3.9.0
conda activate anfler
```

### 2- Clone all sources

``` 
mkdir /tmp/tributosimple-src
cd  /tmp/tributosimple-src

# module anfler-utils
git clone https://gitlab.anfler.com.ar:9999/tributosimple/kafka/utils.git

# module anfler-kafka
git clone https://gitlab.anfler.com.ar:9999/tributosimple/kafka/kafka.git

# module anfler-threadpool
git clone https://gitlab.anfler.com.ar:9999/tributosimple/kafka/threadpool.git

# module anfler-db 
git clone https://gitlab.anfler.com.ar:9999/tributosimple/kafka/db.git

# module anfler-scrapping
git clone https://gitlab.anfler.com.ar:9999/tributosimple/pyapi.git

# application
git clone https://gitlab.anfler.com.ar:9999/tributosimple/kafka/tributosimple.git

```

### 3- Install python dependencies
Goto to each folder in **/tmp/tributosimple-src/anfler-*** and run:

```
cd <anfler-project>
conda install --yes --name anfler --file requirements.txt
```
