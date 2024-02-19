/*----------------------------------------------------------------------------
 Jobs Services
 - service: service name
 - fn: function name to be executed for this service, format:
    <full python package name>.<class name>@<class method>
 - entity: entity name. Define for each entity created:
    * topic tributosimple-topic-<entity>
    * table job_<entity>
 -----------------------------------------------------------------------------*/
CREATE TABLE anflerdb.jobs_services (
	id INTEGER auto_increment NOT NULL PRIMARY KEY,
	service VARCHAR(64) NULL,
	fn VARCHAR(128) NOT NULL,
	entity VARCHAR(10) NOT NULL
    )
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;


-- Records sample
INSERT INTO anflerdb.jobs_services(service, fn, entity) VALUES('get_sales', 'anfler_afip.anfler_mis_comprobantes.MisComprobantes@get_sales', 'afip');
INSERT INTO anflerdb.jobs_services(service, fn, entity) VALUES('get_sales2', 'anfler_afip.anfler_comprobantes.Comprobantes@get_sales', 'afip');
INSERT INTO anflerdb.jobs_services(service, fn, entity) VALUES('get_category', 'anfler_afip.anfler_constancia_inscripcion.Constancia@get_category', 'afip');
INSERT INTO anflerdb.jobs_services(service, fn, entity) VALUES('get_activity', 'anfler_afip.anfler_constancia_inscripcion.Constancia@get_activity', 'afip');
INSERT INTO anflerdb.jobs_services(service, fn, entity) VALUES('get_address', 'anfler_afip.anfler_constancia_inscripcion.Constancia@get_address', 'afip');
INSERT INTO anflerdb.jobs_services(service, fn, entity) VALUES('get_image', 'anfler_afip.anfler_constancia_inscripcion.Constancia@get_image', 'afip');
INSERT INTO anflerdb.jobs_services(service, fn, entity) VALUES('ccma', 'anfler_afip.anfler_ccma.CCMA@run', 'afip');

INSERT INTO anflerdb.jobs_services(service, fn, entity) VALUES('echo', 'app.dummy_service.DummyService@echo', 'admin');
INSERT INTO anflerdb.jobs_services(service, fn, entity) VALUES('error', 'app.dummy_service.DummyService@error', 'admin');

COMMIT;
