from selenium import webdriver
from anfler.util.helper import dpath
import json
from os import path
import anfler.util.config.cfg as cfg

DEV = False

cfg.load(["/app/etc/config_scrapper.json"], ignore_errors=True)

ROOT = dpath(cfg.config, "PATH.base.ROOT", "/app")
DOWNLOADS_PATH = dpath(cfg.config, "PATH.base.DOWNLOADS_PATH", "/tmp/")

CHROMEDRIVER_PATH = dpath(cfg.config, "PATH.afip.CHROMEDRIVER_PATH", r"/usr/local/bin/chromedriver")
FIREFOX_PATH = dpath(cfg.config, "PATH.afip.FIREFOX_PATH", "/usr/local/bin/geckodriver")

DRIVERS_ALLOWED = {
    "chrome": webdriver.Chrome,
    "firefox": webdriver.Firefox
}

# ROUTE TO LOG FILE
LOG_FILE = "../test/"
LOG_CONFIG = "../factory/logging_test.json"

# ESTATIC URL AFIP
URL_LOGIN_AFIP = "https://auth.afip.gob.ar/contribuyente_/login.xhtml"

STATUS_OK = 0
STATUS_FAIL = 1

MSG_IN = {
    'message': {
        'header': {
            'auth': {
                'codif': 0,
                'cuit': 0,
                'password': '',
                'type': 'basic'
            },
            'fn': '',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            'browser': 'chrome',
            'from': '01/01/1900',
            'to': '01/01/1900',
        }
    }
}

MSG_OUT = {
    'messages': {
        'status': 0,
        'errors': [],
        'header': {
            'auth': {
                'codif': 0,
                'cuit': 0,
                'password': '',
                'type': 'basic'
            },
            'fn': '',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'id': None,
        'payload': {
            'data': ''
        }
    }
}

d_xpath = {
    "XPATH_REINGRESO": "//*[@id='aIngresarDeNuevo']",
    "XPATH_CUIT_AFIP": "//*[@id='F1:username']",
    "XPATH_CUIT_INVALIDO": "//*[@id='F1:msg']",
    "XPATH_PWD_AFIP": "//*[@id='F1:password']",
    "XPATH_CCMA": "/html/body/main/section[1]/div/div[24]/div/div/div",
    "CLASS_CCMA": "bold",
    "NAME_CCMA": 'CCMA - CUENTA CORRIENTE DE CONTRIBUYENTES MONOTRIBUTISTAS Y AUTONOMOS',
    "NAME_COMPROBANTES": "Comprobantes en línea",
    "NAME_MONOTRIBUTO": "Monotributo",
    "NAME_MIS_COM": "Mis Comprobantes",
    "XPATH_CAL_DEUDA": "/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/form/table/tbody/tr[4]/td/div/input[3]",
    "XPATH_BODY_DEUDA": "/html/body/table[2]/tbody/tr[2]/td[2]/form/table[1]/tbody",
    "XPATH_MONOTRIBUTO": "/html/body/main/section[1]/div/div[14]/div/div/div",
    "XPATH_CAJAS_AFIP": "/html/body/main/section[2]/div/div[*]",
    "XPATH_CONSTANCIAS": "//*[@id='menuLateral']/li[4]/a",
    "XPATH_VER_CONSTANCIA": "//*[@id='bBtn1']",
    "XPATH_CONSTANCIA_INSC": "/html/body/table[2]/tbody/tr[1]",
    "XPATH_ACTIVIDAD_CONSTANCIA": "/html/body/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[16]/td/table/tbody/tr",
    "XPATH_DIRECCION_CONSTANCIA1": "/html/body/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[7]/td/table/tbody/tr[3]",
    "XPATH_DIRECCION_CONSTANCIA2": "/html/body/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[7]/td/table/tbody/tr[4]/td",
    "XPATH_COMPROBANTES": "/html/body/main/section[1]/div/div[8]/div/div/div",
    "XPATH_COMPROBANTES_REPRESENTAR": "//*[@id='contenido']/form/table/tbody/tr[4]/td",
    "XPATH_COMPROBANTES_CONSULTAS": "//*[@id='btn_consultas']",
    "XPATH_COMPROBANTES_CON_FROM": "//*[@id='fed']",
    "XPATH_COMPROBANTES_CON_TO": "//*[@id='feh']",
    "XPATH_FACTURA_C": "/html/body/div[2]/form/div/div/table/tbody/tr[4]/td/select/option[10]",
    "XPATH_PTO_VENTA": "/html/body/div[2]/form/div/div/table/tbody/tr[5]/td/select/option[2]",
    "XPATH_BUSCAR_FACT_C": "/html/body/div[2]/table/tbody/tr/td/input[2]",
    "XPATH_FACTURA_C_VER": ".//html/body/div[2]/div[3]/div/table/tbody/tr[*]/td[7]/input",
    "XPATH_RECIBO_C": "/html/body/div[2]/form/div/div/table/tbody/tr[4]/td/select/option[13]",
    "XPATH_CONSULTA_SIFERE": "//*[@id='servicesContainer']/div[29]",
    "XPATH_CAT": "/html/body/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[10]/td/table/tbody/tr/td[2]/table/tbody/tr/td/font[2]",
    "XPATH_MIS_COMPROBANTES": "/html/body/main/section[1]/div/div[25]/div/div/div/div[2]/h4",
    "XPATH_MISC_EMITIDOS": "//*[@id='btnEmitidos']/div[2]/p",
    "XPATH_MISC_RANGO_FECHA": "//*[@id='fechaEmision']",
    "XPATH_MISC_BUSCAR": "//*[@id='buscarComprobantes']",
    "XPATH_MISC_DCSV": "//*[@id='tablaDataTables_wrapper']/div[1]/div[1]/div/button[1]/span",
    "XPATH_SELECT_CUIT": "//select[@id='selectLogui']"
}

if DEV:
    base_path = path.dirname(__file__)
    path_rutas = "../etc/rutas.json"
    path_rutas = path.join(base_path, path_rutas)
else:
    path_rutas = "/app/etc/rutas.json"

try:
    with open(path_rutas, "r") as f:
        ext_dict = json.loads(f.read())
except Exception:
    ext_dict = d_xpath

inv_xpath = dict()
for k, v in ext_dict.items():
    inv_xpath[v] = k