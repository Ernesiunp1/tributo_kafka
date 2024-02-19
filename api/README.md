# Aplicacion Tributo Simple (API) 

---

## Introduction
TributoSimple (API) is a Python 3 application to expose scraping operations from [Tributo Simple (Backend)](https://gitlab.anfler.com.ar:9999/tributosimple/kafka/tributosimple)

Application use [FastAPI](https://fastapi.tiangolo.com/) for building the api



## Application and dependencies

Main application file is located in  [app/anfler_api.py](app/anfler_api.py). Source code:

Application have the following dependencies:
- Module [anfler-utils](https://gitlab.anfler.com.ar:9999/tributosimple/kafka/utils.git)
- Module [anfler-kafka](https://gitlab.anfler.com.ar:9999/tributosimple/kafka/kafka.git)
- Module [anfler-db](https://gitlab.anfler.com.ar:9999/tributosimple/kafka/db.git)
  



## Installation

Please refer to Devops repo: [README.md](https://gitlab.anfler.com.ar:9999/pingino/tributo-docker/-/blob/master/README.md)


## Configuration


### 1- Configuration files
Application is configured using the following files:
- [etc/config.json](etc/config.json)
  
  Configuration file
- [etc/logging.json](etc/logging.json)
  
These files are documented in [Tributo Simple (Backend)](https://gitlab.anfler.com.ar:9999/tributosimple/kafka/tributosimple)

#### 1.1 File etc/config.json
There are 4 sections to configure:
- kafka
  This section configure Kafka module (kafka client)
  
```
{
  "kafka": {
    "producer": {
      "bootstrap_servers": ["anfler.kafka1:29092"],
      "client_id": "tributo-client-producer",
      "value_serializer":"lambda x: json.dumps(x).encode('utf-8')"
    },
    "producer_topics": ["tributosimple-topic-admin", "tributosimple-topic-afip","tributosimple-topic-arba", "tributosimple-topic-agip"],
    "debug": false,
    "init_retry_max": 10,
    "init_retry_delay": 60
  },

}
```
  
  - **producer** is documented in [Kafka Client](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html)
  - **producer_topics** List of topics to send messages
  - **debug** enable debug on loggers "anfler.kafka", please use [etc/logging.json](etc/logging.json)
  - **init_retry_max** and **init_retry_delay** retry options used when application start, these values are used only when app is initializing, allowing to "wait" for Kafka server

- db
  
  Please refer to [Tributo Simple (Backend)](https://gitlab.anfler.com.ar:9999/tributosimple/kafka/tributosimple)
- logging
  
  Please refer to [Tributo Simple (Backend)](https://gitlab.anfler.com.ar:9999/tributosimple/kafka/tributosimple)  
- jwt
  All endpoints are secured with [JWT Token-based Authentication](https://pyjwt.readthedocs.io), **ALL PEM files MUST be the same configured in PHP app** 
  
  
```
{
  "jwt": {
        "PRIVATE_KEY":"",
        "PRIVATE_KEY_FILE":"/api/etc/private.pem.txt",
        "PRIVATE_PASS": "dusEZzcDqhSAIJeY",
        "PUBLIC_KEY_FILE": "/api/etc/public.pem.txt",
        "ALGORITHM": "RS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": 5
    }
}
```
  - **PRIVATE_KEY** Private key (PEM text)
  - **PRIVATE_KEY_FILE** Absolut path to private pem file 
  - **PRIVATE_PASS** Password for private key
  - **PUBLIC_KEY_FILE** Absolut path to public pem file
  - **ALGORITHM** Algorithm to decode/encode
  - **ACCESS_TOKEN_EXPIRE_MINUTES** Token expiration
  
Notes:
- Public pem file should look like:
```
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA4dEabtI7v9aty3XjkIvP
...
...
-----END PUBLIC KEY-----

```
- Priate pem file should look like:
```
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIJrTBXBgkqhkiG9w0BBQ0wSjApBgkqhkiG9w0BBQwwHAQIwqnqTnE+J6ECAggA
...
...
-----END ENCRYPTED PRIVATE KEY-----

```


#### 1.2 File etc/loggin.json
  This file contains all logger defined for the application, see https://docs.python.org/3/library/logging.config.html#module-logging.config



## Application build and installation
Please see [tributo-docker](https://gitlab.anfler.com.ar:9999/pingino/tributo-docker)

## Application start 

After install all modules, run 
```
cd /api
./ruun_uvicorn.sh

```

## Environment properties
Application needs the following environment variables:

- **APP_HOME**: Application root folder
- **APP_LOG**: Application log folder ({APP_HOME}/logs)
- **APP_CONFIG_FILE**: Application configuration file ({APP_HOME}/etc/config.json)
- **APP_CONFIG_LOG_FILE**: Application logginf configuration ({APP_HOME}/etc/logging.json)


See [docker-compose.yml](https://gitlab.anfler.com.ar:9999/pingino/tributo-docker)
  

## Testing application

- Get a token from PHP server
- Do a request to application, for example:
``` 
curl -X GET 'http://anfler.api:80/me' --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImN0eSI6IkpXVCJ9.eyJpYXQiOjE2MTQ4MTQwNjEsImV4cCI6MTYxNDgyMTI2MSwicm9sZXMiOlsiUk9MRV9VU0VSIl0sInVzZXJuYW1lIjoia2V2aW50ZXJ1ZWwzNDVAZ21haWwuY29tIiwiaWQiOjd9.MQOJAKwDvXE6Ml-HhcXud2_FVix4eDr4ETDiPxBcy9JM2pVuJ33xVta2pNRiIK2Mo_kJDEpoQZJHk8jI1ClJ59t5Qu9ktazCVUHNrbd1cjQp1PrNLUqIcCVcREgoNcGENiayQ_Z9X5V-2vbUVywFb0seZksi6nnO_mBopFL3nJM-Pc4suBowgXpHqEG2DRaggb7Cmaqe_i0JJgSJpzVgoonriasj-nPVA5-CWAvUjAMWHgJTKoPDaGDz59z23fLVG7wBDEfriSTbgGhg-d-oPEOzZh6TyJWsjGG2PqWqP2muAhxM9NjFt1jcVd-r-roWTLZsssASRITyWO6O8nmxn1QOGzI7IZcrsuKhDsBGKX7iGKCzYPYu5PlkHK5MtC_vtr0nuL4YVIclF8VIw0WwfLrDJh1mZYTaoI-tbDggdVLhvY9_w97uvH7li0BSrmqUy0N-frG_la5bMiUOEf_AHrdZ-VtQzk7uwA3-DU23aw-vcsYHLA4pH1yYTyrCPbUF506iSUC2Kf0G8WuIOSRjNoqTx5VeUMwlFoapXPAltD8vFExwf4NSkBP4VOyJy9Mxq_WRl1XpaSF1fhg0EIJBwYfvZkNruUJz6TWeKEV6tSHuUAlSVyjvN2lGZbTInTKCZYjqRKxpKvNirKs1CqdKv6hMRyMAma0BFuwGkcDGsP0'
```

Response:
``` 
{
  "token_data": {
    "username": "kevinteruel345@gmail.com",
    "exp": 1614821261,
    "id": 7,
    "iat": 1614814061,
    "roles": [
      "ROLE_USER"
    ]
  },
  "datetime_utc": "2021-03-03T23:28:55.764764"
}

```


## API definition 

Located in **http://\<API_HOST\>:\<API_PORT\>/docs**, for example http://anfler.api:80/docs 


