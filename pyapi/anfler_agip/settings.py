from selenium import webdriver
from anfler_base.settings import *
from anfler.util.helper import dpath
import anfler.util.config.cfg as cfg

cfg.load(["/app/etc/config_scrapper.json"], ignore_errors=True)

ROOT = dpath(cfg.config, "PATH.agip.ROOT", "/app")
DOWNLOADS_PATH = dpath(cfg.config, "PATH.agip.DOWNLOADS_PATH", "/tmp/")
CHROMEDRIVER_PATH = dpath(cfg.config, "PATH.agip.CHROMEDRIVER_PATH", r"/usr/local/bin/chromedriver")
FIREFOX_PATH = dpath(cfg.config, "PATH.agip.FIREFOX_PATH", "/usr/local/bin/geckodriver")

DRIVERS_ALLOWED = {
    "chrome": webdriver.Chrome,
    "firefox": webdriver.Firefox
}

OPTIONS_DRIVER = {
    "chrome": {
        "options": {
            "profile.default_content_settings.popup": 0,
            "download.default_directory": DOWNLOADS_PATH,
            "plugins.always_open_pdf_externally": True
        },
        "path": CHROMEDRIVER_PATH,
    },
    "firefox": {
        "options": {
            "browser.download.folderList": 2,
            "browser.download.manager.showWhenStarting": False,
            "browser.download.dir": DOWNLOADS_PATH
        },
        "path": FIREFOX_PATH
    }
}

# ROUTE TO LOG FILE
LOG_FILE = "../test/test.log"

# URL ESTATICA DE ARBA
URL_LOGIN_AGIP = "https://clusterapw.agip.gob.ar/claveciudad/"

# ############# XPATHS DE AGIP
XPATH_CUIT_LOGIN = "//*[@id='cuit']"
XPATH_PWD_LOGIN = "//*[@id='clave']"
XPATH_APLICACIONES = "/html/body/div/div[3]/div/b/b/b/div[2]/div[*]/div[1]"
XPATH_ARCIBA = "//*[@id='aplicaciones']/div[11]/div[2]"
XPATH_ARCIBA_SELECT_REGIMEN = "//*[@id='regimenCo']"
XPATH_ARCIBA_BUSCAR = "//*[@id='botonBuscarCo']/span"
XPATH_ARCIBA_HERRAMIENTAS = "//*[@id='tablaRetenciones_botonHerramientas']/a/i"
XPATH_ARCIBA_CSV = "//*[@id='tablaRetenciones_botonExcel']"
XPATH_ARCIBA_DESDE = "//*[@id='fechaDesdeCo']"
XPATH_DDJJ_PRESENTADA = "//*[@id='gridview-1066-hd-Presentada']/td/div/div/div"
XAPTH_ULTIMA_PRESENTADA = "//*[@id='gridview-1066-bd-Presentada']/td/table/tbody/tr[2]/td[2]/div"
XPATH_ESICOL_DDJJ_TREE = "/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[1]/div/div/div[1]/div[5]/div/table/tbody/tr[*]/td/div/span"
XPATH_ESICOL_SALDO_RESULTANTE = "//*[@id='gridview-1102-bd-3-Saldo resultante']/td/table/tbody/tr[3]"

CLASS_DDJJ_PRESENTADA_PERIODO = "x-grid-cell-inner "
XPATH_VEP_CALCULAR = "//*[@id='button-1112-btnInnerEl']"
XPATH_VEP_VEP = "//*[@id='radiofield-1118-inputEl']"
XPATH_DIC_PAGOS = {
    "pagomiscuentas": "//*[@id='radiofield-1121-inputEl']",
    "interbanking": "//*[@id='radiofield-1122-inputEl']",
    "link": "//*[@id='radiofield-1123-inputEl']"
}

XPATH_CERRAR_DEFAULT = "//*[@id='tool-1091']"
XPATH_PANEL_LATERAL_DDJJ = "//*[@id='tool-1056-toolEl']"
XPATH_NUEVA_DDJJ = "//span[@id='mainNuevaDdjjBtn-btnInnerEl']"
XPATH_DDJJ_ANIO_FLECHA = "//*[@id='ext-gen1271']"
CLASS_DDJJ_ANIOS = "x-boundlist-item"
XPATH_DDJJ_MES_FLECHA = "//*[@id='ext-gen1273']"

XPATH_PERIODOS_IMPAGOS = "//*[@id='button-1049-btnInnerEl']"
CLASS_ESICOL_INNER = "x-grid-cell-inner "

C_XPATH_LOGIN_AGIP = (XPATH_CUIT_LOGIN, XPATH_PWD_LOGIN)

inv_xpath = dict()
for k, v in d_xpath.items():
    inv_xpath[v] = k
