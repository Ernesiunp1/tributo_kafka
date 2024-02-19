/*----------------------------------------------------------------------------
 Jobs logs (one table for each entity)
 - id: incremental number
 - msg_id: request messag id
 - user: request user
 - state: state, 0 (pendind), 1 (finished)
 - service: service name (defined in table jobs_services)
 - fn: function name executed (defined in table jobs_services)
 - entity: entity (defined in table jobs_services)
 - payload_in: request payload (JSON)
 - payload_out: response payload (JSON)
 - status: status (return code)
 - errors: response errors (JSON)
 - job_id: internal job id for the request
 - kafka_key: Kafka key
 - kafka_offset: Kafka offset
 - kafka_partition: Kafka partition
 - dt_created: record creation timestamp
 - dt_updated: record update timestamp
 -----------------------------------------------------------------------------*/


/* ---------------------------------------------------------------------------
 *   Jobs AFIP
 * ---------------------------------------------------------------------------*/
CREATE TABLE anflerdb.jobs_afip (
	id INTEGER auto_increment NOT NULL PRIMARY KEY,
	msg_id VARCHAR(64) NULL,
	user VARCHAR(64) DEFAULT 'UNKNOWN' NOT NULL,
	state INT DEFAULT 0 NOT NULL,
	service VARCHAR(128) NOT NULL,
	fn VARCHAR(128) NOT NULL,
	entity VARCHAR(10) NOT NULL,
	payload_in JSON NOT NULL,
	payload_out JSON NOT NULL,
	status INT DEFAULT 0 NOT NULL,
	errors JSON,
	job_id VARCHAR(64) NULL,
	kafka_key VARCHAR(100) NULL,
	kafka_offset INT DEFAULT -1 NOT NULL,
	kafka_partition INT DEFAULT -1 NOT NULL,
	dt_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	dt_updated TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

/* ---------------------------------------------------------------------------
 *   Jobs ARBA
 * ---------------------------------------------------------------------------*/
CREATE TABLE anflerdb.jobs_arba (
	id INTEGER auto_increment NOT NULL PRIMARY KEY,
	msg_id VARCHAR(64) NULL,
	user VARCHAR(64) DEFAULT 'UNKNOWN' NOT NULL,
	state INT DEFAULT 0 NOT NULL,
	service VARCHAR(128) NOT NULL,
	fn VARCHAR(128) NOT NULL,
	entity VARCHAR(10) NOT NULL,
	payload_in JSON NOT NULL,
	payload_out JSON NOT NULL,
	status INT DEFAULT 0 NOT NULL,
	errors JSON,
	job_id VARCHAR(64) NULL,
	kafka_key VARCHAR(100) NULL,
	kafka_offset INT DEFAULT -1 NOT NULL,
	kafka_partition INT DEFAULT -1 NOT NULL,
	dt_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	dt_updated TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

/* ---------------------------------------------------------------------------
 *   Jobs AGIP
 * ---------------------------------------------------------------------------*/
CREATE TABLE anflerdb.jobs_agip(
	id INTEGER auto_increment NOT NULL PRIMARY KEY,
	msg_id VARCHAR(64) NULL,
	user VARCHAR(64) DEFAULT 'UNKNOWN' NOT NULL,
	state INT DEFAULT 0 NOT NULL,
	service VARCHAR(128) NOT NULL,
	fn VARCHAR(128) NOT NULL,
	entity VARCHAR(10) NOT NULL,
	payload_in JSON NOT NULL,
	payload_out JSON NOT NULL,
	status INT DEFAULT 0 NOT NULL,
	errors JSON,
	job_id VARCHAR(64) NULL,
	kafka_key VARCHAR(100) NULL,
	kafka_offset INT DEFAULT -1 NOT NULL,
	kafka_partition INT DEFAULT -1 NOT NULL,
	dt_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	dt_updated TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;

/* ---------------------------------------------------------------------------
 *   Jobs ADMIN
 * ---------------------------------------------------------------------------*/
CREATE TABLE anflerdb.jobs_admin(
	id INTEGER auto_increment NOT NULL PRIMARY KEY,
	msg_id VARCHAR(64) NULL,
	user VARCHAR(64) DEFAULT 'UNKNOWN' NOT NULL,
	state INT DEFAULT 0 NOT NULL,
	service VARCHAR(128) NOT NULL,
	fn VARCHAR(128) NOT NULL,
	entity VARCHAR(10) NOT NULL,
	payload_in JSON NOT NULL,
	payload_out JSON NOT NULL,
	status INT DEFAULT 0 NOT NULL,
	errors JSON,
	job_id VARCHAR(64) NULL,
	kafka_key VARCHAR(100) NULL,
	kafka_offset INT DEFAULT -1 NOT NULL,
	kafka_partition INT DEFAULT -1 NOT NULL,
	dt_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	dt_updated TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;