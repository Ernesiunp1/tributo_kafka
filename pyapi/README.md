# tributo_simple

## Desarrollo de web scrapping para la consultora ANFLER
## Usando Python 3.8, Selenium 3.141.0, requests 2.24.0

# CONFIGURACION IMPORTANTE PARA INSTALACIÓN:

luego de clonar el proyecto tendra que ajustar sus variables de entorno al proyecto
para ello haga lo siguiente:

- en el archivo settings.py del directorio anfler_base:
    - Indicar el directorio base donde se encuentra el proyecto ej. ROOT = "/app"
    - Indicar el DOWNLOAD_PATH a la ruta absoluta de descarga ej. DOWNLOADS_PATH = "/home/victor/PycharmProjects/ANFLER-APP/anfler-webscrap/etc/tmp/"

- en el archivo settings.py del directorio anfler_afip:
    - Indicar el directorio base donde se encuentra el proyecto ej. ROOT = "/app"
    - Indicar el DOWNLOAD_PATH a la ruta absoluta de descarga ej. DOWNLOADS_PATH = "/home/victor/PycharmProjects/ANFLER-APP/anfler-webscrap/etc/tmp/"
    - Indicar el path absoluto a la ubicacion del driver de chromedriver ej. CHROMEDRIVER_PATH = r"/usr/bin/chromedriver"
    - Indicar el path absoluto a la ubicacion del driver de firefox ej. FIREFOX_PATH = "geckodriver"

- en el archivo settings.py del directorio anfler_arba:
    - Indicar el directorio base donde se encuentra el proyecto ej. ROOT = "/app"
    - Indicar el DOWNLOAD_PATH a la ruta absoluta de descarga ej. DOWNLOADS_PATH = "/home/victor/PycharmProjects/ANFLER-APP/anfler-webscrap/etc/tmp/"
    - Indicar el path absoluto a la ubicacion del driver de chromedriver ej. CHROMEDRIVER_PATH = r"/usr/bin/chromedriver"
    - Indicar el path absoluto a la ubicacion del driver de firefox ej. FIREFOX_PATH = "geckodriver"


# RECOMENDACIÓN:

- Este modulo se desarrollo en paralelo a los modulos anfler-tributosimple, anfler-db, anfler-kafka, anfler-threadpool, anfler-utils y por tanto compartin la misma ruta base por default "/app" por lo tanto se recomienda mantener esta configuración e instalar este modulo junto a los antes indicados.

# USO:

cada servicio debe ser instanciado mediante un mensaje con la siguiente estructura base:

mensaje = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit1,
                'password': pwd1,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_afip.anfler_comprobantes.Comprobantes@get_sales',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            'from': '01/09/2020',
            'to': '10/11/2020',
        },
    },
}

donde son imprescindible los campos "cuit", "password" del header y de ser necesaria informacion adicional en el "payload"

el manejo de la configuracion de cada servicio se hace desde el archivo config_afip.json ubicado en el directorio "etc", funciona de manera jerarquica por lo cual que diferenciado cada metodo de acuerdo a las necesidades puntuales de cada servicio.


### Las siguientes clases han sido creadas y pueden o no tener varios metodos funcionales internamente.

Hay un modulo base que sirve de patron para cada una de las clases, luego un modulo por cada organismo
a incluir, dentro de cada organismo existen clases que abordan las diversas consultas posibles en los mismos
existen varios archivos settings.py, el base incluye una configuracion generica que debera ampliarse en cada
archivo settings dentro de los organismos.
en el modulo de test hay un archivo con ejemplo de prueba de cada clase y en el archivo ejemplo_kafka.py se
hayam 2 mensajes protitipo de los que seran recibidos para ejectuar dichas pruebas.


### Modulos, clases y metodos actuales:

- anfler_base
    - anfler_baseclass
    - decorators
    	- random_wait
    - settings
- anfler_afip
    - anfler_ccma
    	- run
    - anfler_comprobantes
    	- get_sales
    	- get_image
    	- get_purchases
    - anfler_constancia_inscripcion
    	- get_activity
    	- get_address
    	- get_category
    - anfler_login
	- run
    - anfler_mis_comprobantes
    	- get_sales
    	- get_purchases
    - anfler_alta_monotributo
    	- step_1
    	- biometric
    	- registral_system
    - anfler_sifere_consultas
    	- get_jurisdiccion
    - settings
- anfler_arba
    - login
    	- run
    - ccma
    	- resume
    	- positive_balance
    - settings
- etc	
    - logging
        - config.py
        - logging.json
        - logging_wrapper.py
    - config.json
    - config_afip.json
-factory
    - factory
- test
    - test1
- exceptions
    - exceptions
- ejemplo_kafka.py
    
## Notas: 
 * La clase base sera luego dividida en 2 clases, una con los metodos estaticos y sera llamada utils.
 * Los archivos producer, consumer, ejemplo y fake_data incluidos test requieren que esten activos (solo util para pruebas, para productivo usar configuración propia del modulo kafka).
 * Los Servidores de kafka y zookeeper, estan con un topico afip.ccma los comandos de activacion default son:
   * comando_1 = "bin/zookeeper-server-start.sh config/zookeeper.properties"
   * comando_2 = "JMX_PORT=8004 bin/kafka-server-start.sh config/server.properties"
   * comando_3(opcional) = "bin/cmak -Dconfig.file=conf/application.conf -Dhttp.port=8080"


# CONFIGURACION DE ENTORNO PARA DESARROLLO ACTUALIZADO AL 29/10/2022

1._ Crear entorno virtual en Anaconda conPython 3.9
2._ Crear estructura del proyecto como sigue:
ANFLER-APP
		anfler-webscrap
		utils

En la carpeta anfler webscrap copiar los archivos del repositorio pyapi, 
en la carpeta utils poner los archivos del repositorio utils.

3._ Navegar hasta la carpeta utils y ejecutar python setup.py install
4._ Navegar hasta la carpeta anfler-webscrap y ejecutar pip install -r requirements.txt
5._ Ira a al directorio etc y generar una copia al archivo config_scrapper.json para trabajar en desarrollo
6._ Actualizar settings en el archivo anterior: 
	
    "DOWNLOADS_PATH"
    "ROOT"
	"CHROMEDRIVER_PATH" 
    "FIREFOX_PATH" 

7._ En el archivo anfler_baseclass.py, actualizar el nombre del archivo config_file_2 que correspode al archivo anterior
8._ en el archivo el archivo settings.py de la carpeta anfler_base, cambiar la modalidad de trabajo a 
    desarrollo de false a true, ajustado al tipo de trabajo necesitado, esto permite seleccionar diferentes archivos de 
    configuración para diferentes entornos de trabajo.

9._ instalar googlechrome versiones igual o inferior 89.0.4389 y su correpondiente chromedriver


10._ Ubicar el archivo chromedriver dentro de la carpeta driver del proyecto (aconsejable y opcional)


## Nota: Si se desea alternar entre modo headless o visual, esto se ajusta en el archivo config_afip.json
	buscando el servicio corespondientes y cambiado la key: headless entre true y false 