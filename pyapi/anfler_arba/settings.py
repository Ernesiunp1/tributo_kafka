from selenium import webdriver
from anfler_base.settings import *
from anfler.util.helper import dpath
import anfler.util.config.cfg as cfg

cfg.load(["/app/etc/config_scrapper.json"], ignore_errors=True)

ROOT = dpath(cfg.config, "PATH.arba.ROOT", "/app")
DOWNLOADS_PATH = dpath(cfg.config, "PATH.arba.DOWNLOADS_PATH", "/tmp/")
CHROMEDRIVER_PATH = dpath(cfg.config, "PATH.arba.CHROMEDRIVER_PATH", r"/usr/local/bin/chromedriver")
FIREFOX_PATH = dpath(cfg.config, "PATH.arba.FIREFOX_PATH", "/usr/local/bin/geckodriver")

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
URL_LOGIN_ARBA = "https://sso.arba.gov.ar/Login/login?service=http%3A//www.arba.gov.ar/DatosContacto/datoscontacto.asp%3FFrame%3Dno%26InfoContri%3Dsi%26App%3D12%26urlretorno%3D%26urlsiguiente%3Dhttps%253A%252F%252Fwww%252Earba%252Egov%252Ear%252FGestionar%252FGestionar%255FDefault%252Easp"

# ############# XPATHS DE ARBA
# XPATH LOGIN
XPATH_SELECT_CUIT = "//select[@id='selectLoguin']"
XPATH_DNI = "//input[@id='CUIT']"
XPATH_PWD = "//input[@id='clave_Cuit']"
XPATH_CUENTA_CORRIENTE = "//*[@id='accordionInmo']/div/div[2]"
XPATH_SALDO_FAVOR_TOTAL = "/html/body/app-root/div[1]/app-gestionarcontribuyente/app-gestionar/div/div[2]/app-impuestos/div/div/div[3]/div[1]/div/div/div[3]/span"
XPATH_SALDO_FAVOR_IIBB = "/html/body/app-root/div[1]/app-gestionarcontribuyente/app-gestionar/div/div[2]/app-impuestos/div/div/div[2]/app-ingresosbrutos/div/div[1]/a/div/div[3]/span"
XPATH_DEUDA_IIBB = "/html/body/app-root/div[1]/app-gestionarcontribuyente/app-gestionar/div/div[2]/app-impuestos/div/div/div[2]/app-ingresosbrutos/div/div[1]/a/div/div[2]/span"
XPATH_USUARIO_INVALIDO = "/html/body/div[1]/div[2]/div[1]/font"
# XPATH DECLARACION JURADA
XPATH_IIBB = "/html/body/app-root/div[1]/app-gestionarcontribuyente/app-gestionar/div/div[1]/app-menu-secundario/nav/ul/app-arbol-menu/li[1]/a"
XPATH_IIBB_PRES_DDJJ = "//*[@id='#child12']/app-arbol-menu/li[2]/a/span"
XPATH_IIBB_PRES_DDJJ_2 = "/html/body/div[1]/div[1]"
XPATH_IIBB_PRES_ANTICIPO = "/html/body/div[2]/div[1]"
XPATH_IIBB_PRES_ANTICIPO_INICIO = "/html/body/div[3]/div[1]"
XPATH_IIBB_PRES_ANTICIPO_BTN_INICIAR = "//*[@id='siguiente']"
XPATH_IIBB_PRES_SELECT_1 = "//*[@id='regimen']"
XPATH_IIBB_PRES_SELECT_2 = "//*[@id='anioMensual']"
XPATH_IIBB_PRES_SELECT_3 = "//*[@id='mes']"
XPATH_IIBB_PRES_DETALLE_POP2 = "/html/body/div[13]"
XPATH_IIBB_PRES_DETALLE_CARGA = "//*[@id='btnActividades']/a"
XPATH_IIBB_PRES_DETALLE_CARGA_TEXT_EDIT = "//*[@id='tablaAlicuotas']/tbody/tr/td[*]"
XPATH_IIBB_PRES_DETALLE_CARGA_EDIT = "//*[@id='tablaAlicuotas']/tbody/tr/td[9]/span"
XPATH_IIBB_PRES_DETALLE_EDIT_M_IMPON = "//*[@id='imImponible']"
XPATH_IIBB_PRES_EDIT_M_IMPON_BUT = "//*[@id='siguiente']"
XPATH_IIBB_PRES_EDIT_BUTT_BACK = "//*[@id='button1']"
XPATH_IIBB_PRES_EDIT_BUTT_DEDUCC = "//*[@id='btnDeducciones']/a"
XPATH_IIBB_PRES_DEDUCC_CARGA = "//*[@id='deduccionesCargaManualBtn']/a"
XPATH_IIBB_PRES_EDIT_CHK = "//*[@id='esModificada']"
XPATH_IIBB_PRES_EDIT_SELECT = "//*[@id='aliModificada']"
XPATH_IIBB_PRES_DDJJ_RESUMEN = "//*[@id='resumen']"
XPATH_IIBB_PRES_DEDUCC_VOLVER = "//*[@id='volver']"
XPATH_IIBB_PRES_DDJJ_ENVIAR = "//*[@id='benviar']"
# XPATHS_VEP
XPATH_PAGA_VEP_ARBA = "//*[@id='datatable-0']/tbody/tr/td[5]/button"
XPATH_VEP_ARBA_ELECTRONICO = "//*[@id='pago_E']"
XPATH_VEP_ARBA_TODOS = "//*[@id='check_cuota_3']"
XPATH_VEP_ARBA_CONTINUAR = "//*[@id='btnContinuar']"
XPATH_VEP_ARBA_LIBRE = "/html/body/div/div[2]/div[3]/p"
NAME_VEP_LIBRE = "OBJETO SIN DEUDA A LIQUIDAR"
XPATH_VEP_ARBA_MEDIOS = "//*[@id='tablaMediosPE']/tbody/tr/td[*]/a/img"
XPATH_VEP_CODIGO = "/html/body/div/div[2]/div[3]/table[2]/tbody/tr[2]/td"

#XPATH LIQUIDACION MENSUAL
XPATH_IIBB_LIQUIDACION = "/html/body/div[1]/div[3]"
XPATH_IIBB_LIQUIDACION_OBLIGA = "/html/body/div[5]/div[1]"
XPATH_IIBB_OBLIG_PEST = "//*[@id='ui-id-2']"
XPATH_IIBB_OBLIG_SELECT_ANIO_DESDE = "//*[@id='anioMensualDesde']"
XPATH_IIBB_OBLIG_SELECT_ANIO_HASTA = "//*[@id='anioMensualHasta']"
XPATH_IIBB_OBLIG_SELECT_MES_DESDE = "//*[@id='mesDesde']"
XPATH_IIBB_OBLIG_SELECT_MES_HASTA = "//*[@id='mesHasta']"
XPATH_IIBB_OBLIGACION_BUSCAR = "//*[@id='buscar']"
XPATH_IIBB_OBLIGACION_VER = "//*[@id='resultados']/tbody/tr[1]/td[9]/span"

#XPATHS DEDUCCIONES Y PERCEPCIONES
XPATH_IIBB_DEDUCCIONES = "//*[@id='#child12']/app-arbol-menu/li[3]/a/span"
XPATH_DEDUC_ROL_SELECT = "//*[@id='rol_check']/div/div/fieldset[1]/fieldset/div[2]/label[2]/select"
XPATH_DEDUC_ROL_SELECC = "//*[@id='seleccionar']"
XPATH_DEDUC_DEDUC = "//*[@id='cmenu']/li[3]/a"
XPATH_DEDUC_DEDUC_DESC = "//*[@id='cmenu']/li[3]/ul/li[1]/a"
XPATH_DEDUC_DESC_ANIO = "/html/body/div/form/table/tbody/tr[3]/td[2]/input[1]"
XPATH_DEDUC_DESC_MES = "/html/body/div/form/table/tbody/tr[3]/td[2]/input[2]"
XPATH_DEDUC_CONSULTAR = "/html/body/div/form/table/tbody/tr[5]/td/input"
XPATH_DEDUC_DESCARGAR = "/html/body/div/form/table/tbody/tr[3]/td/input[2]"
XPATH_DEDUC_NO = "/html/body/div/table[1]/tbody/tr[2]/td"


# COMBOS XPATHS
C_XPATH_LOGIN_ARBA = (XPATH_SELECT_CUIT, XPATH_DNI, XPATH_PWD)

d_xpath = {
    "XPATH_SELECT_CUIT": "//select[@id='selectLoguin']",
    "XPATH_DNI": "//input[@id='CUIT']",
    "XPATH_PWD": "//input[@id='clave_Cuit']",
    "XPATH_CUENTA_CORRIENTE": "//*[@id='accordionInmo']/div/div[2]",
    "XPATH_SALDO_FAVOR_TOTAL": "/html/body/app-root/div[1]/app-gestionarcontribuyente/app-gestionar/div/div[2]/app-impuestos/div/div/div[3]/div[1]/div/div/div[3]/span",
    "XPATH_SALDO_FAVOR_IIBB": "/html/body/app-root/div[1]/app-gestionarcontribuyente/app-gestionar/div/div[2]/app-impuestos/div/div/div[2]/app-ingresosbrutos/div/div[1]/a/div/div[3]/span",
    "XPATH_DEUDA_IIBB": "/html/body/app-root/div[1]/app-gestionarcontribuyente/app-gestionar/div/div[2]/app-impuestos/div/div/div[2]/app-ingresosbrutos/div/div[1]/a/div/div[2]/span",
    "XPATH_USUARIO_INVALIDO": "/html/body/div[1]/div[2]/div[1]/font",
    "XPATH_IIBB": "/html/body/app-root/div[1]/app-gestionarcontribuyente/app-gestionar/div/div[1]/app-menu-secundario/nav/ul/app-arbol-menu/li[1]/a",
    "XPATH_IIBB_PRES_DDJJ": "//*[@id='#child12']/app-arbol-menu/li[2]/a/span",
    "XPATH_IIBB_PRES_DDJJ_2": "/html/body/div[1]/div[1]",
    "XPATH_IIBB_PRES_ANTICIPO": "/html/body/div[2]/div[1]",
    "XPATH_IIBB_PRES_ANTICIPO_INICIO": "/html/body/div[3]/div[1]",
    "XPATH_IIBB_PRES_ANTICIPO_BTN_INICIAR": "//*[@id='siguiente']",
    "XPATH_IIBB_PRES_SELECT_1": "//*[@id='regimen']",
    "XPATH_IIBB_PRES_SELECT_2": "//*[@id='anioMensual']",
    "XPATH_IIBB_PRES_SELECT_3": "//*[@id='mes']",
    "XPATH_IIBB_PRES_DETALLE_POP2": "/html/body/div[13]",
    "XPATH_IIBB_PRES_DETALLE_CARGA": "//*[@id='btnActividades']/a",
    "XPATH_IIBB_PRES_DETALLE_CARGA_TEXT_EDIT": "//*[@id='tablaAlicuotas']/tbody/tr/td[*]",
    "XPATH_IIBB_PRES_DETALLE_CARGA_EDIT": "//*[@id='tablaAlicuotas']/tbody/tr/td[9]/span",
    "XPATH_IIBB_PRES_DETALLE_EDIT_M_IMPON": "//*[@id='imImponible']",
    "XPATH_IIBB_PRES_EDIT_M_IMPON_BUT": "//*[@id='siguiente']",
    "XPATH_IIBB_PRES_EDIT_BUTT_BACK": "//*[@id='button1']",
    "XPATH_IIBB_PRES_EDIT_BUTT_DEDUCC": "//*[@id='btnDeducciones']/a",
    "XPATH_IIBB_PRES_DEDUCC_CARGA": "//*[@id='deduccionesCargaManualBtn']/a",
    "XPATH_IIBB_PRES_EDIT_CHK": "//*[@id='esModificada']",
    "XPATH_IIBB_PRES_EDIT_SELECT": "//*[@id='aliModificada']",
    "XPATH_IIBB_PRES_DDJJ_RESUMEN": "//*[@id='resumen']",
    "XPATH_IIBB_PRES_DEDUCC_VOLVER": "//*[@id='volver']",
    "XPATH_IIBB_PRES_DDJJ_ENVIAR": "//*[@id='benviar']",
    "XPATH_PAGA_VEP_ARBA": "//*[@id='datatable-0']/tbody/tr/td[5]/button",
    "XPATH_VEP_ARBA_ELECTRONICO": "//*[@id='pago_E']",
    "XPATH_VEP_ARBA_TODOS": "//*[@id='check_cuota_3']",
    "XPATH_VEP_ARBA_CONTINUAR": "//*[@id='btnContinuar']",
    "XPATH_VEP_ARBA_LIBRE": "/html/body/div/div[2]/div[3]/p",
    "NAME_VEP_LIBRE": "OBJETO SIN DEUDA A LIQUIDAR",
    "XPATH_VEP_ARBA_MEDIOS": "//*[@id='tablaMediosPE']/tbody/tr/td[*]/a/img",
    "XPATH_VEP_CODIGO": "/html/body/div/div[2]/div[3]/table[2]/tbody/tr[2]/td",
    "XPATH_IIBB_LIQUIDACION": "/html/body/div[1]/div[3]",
    "XPATH_IIBB_LIQUIDACION_OBLIGA": "/html/body/div[5]/div[1]",
    "XPATH_IIBB_OBLIG_PEST": "//*[@id='ui-id-2']",
    "XPATH_IIBB_OBLIG_SELECT_ANIO_DESDE": "//*[@id='anioMensualDesde']",
    "XPATH_IIBB_OBLIG_SELECT_ANIO_HASTA": "//*[@id='anioMensualHasta']",
    "XPATH_IIBB_OBLIG_SELECT_MES_DESDE": "//*[@id='mesDesde']",
    "XPATH_IIBB_OBLIG_SELECT_MES_HASTA": "//*[@id='mesHasta']",
    "XPATH_IIBB_OBLIGACION_BUSCAR": "//*[@id='buscar']",
    "XPATH_IIBB_OBLIGACION_VER": "//*[@id='resultados']/tbody/tr[1]/td[9]/span",
    "XPATH_IIBB_DEDUCCIONES": "//*[@id='#child12']/app-arbol-menu/li[3]/a/span",
    "XPATH_DEDUC_ROL_SELECT": "//*[@id='rol_check']/div/div/fieldset[1]/fieldset/div[2]/label[2]/select",
    "XPATH_DEDUC_ROL_SELECC": "//*[@id='seleccionar']",
    "XPATH_DEDUC_DEDUC": "//*[@id='cmenu']/li[3]/a",
    "XPATH_DEDUC_DEDUC_DESC": "//*[@id='cmenu']/li[3]/ul/li[1]/a",
    "XPATH_DEDUC_DESC_ANIO": "/html/body/div/form/table/tbody/tr[3]/td[2]/input[1]",
    "XPATH_DEDUC_DESC_MES" : "/html/body/div/form/table/tbody/tr[3]/td[2]/input[2]",
    "XPATH_DEDUC_CONSULTAR": "/html/body/div/form/table/tbody/tr[5]/td/input",
    "XPATH_DEDUC_DESCARGAR": "/html/body/div/form/table/tbody/tr[3]/td/input[2]",
    "XPATH_DEDUC_NO": "/html/body/div/table[1]/tbody/tr[2]/td"
}

inv_xpath = {}
for k, v in d_xpath.items():
    inv_xpath[v] = k
