from selenium import webdriver
from anfler_base.settings import *
from anfler.util.helper import dpath
import anfler.util.config.cfg as cfg

cfg.load(["/app/etc/config_scrapper.json"], ignore_errors=True)

ROOT = dpath(cfg.config, "PATH.afip.ROOT", "/app")
DOWNLOADS_PATH = dpath(cfg.config, "PATH.afip.DOWNLOADS_PATH", "/tmp/")
CHROMEDRIVER_PATH = dpath(cfg.config, "PATH.afip.CHROMEDRIVER_PATH", r"/usr/local/bin/chromedriver")
FIREFOX_PATH = dpath(cfg.config, "PATH.afip.FIREFOX_PATH", "/usr/local/bin/geckodriver")

PORT = "9515"

DRIVERS_ALLOWED = {
    "chrome": webdriver.Chrome,
    "firefox": webdriver.Firefox
}
OPTIONS_DRIVER = {
    "chrome": {
        "options": {
            "profile.default_content_settings.popup": 0,
            "download.default_directory": DOWNLOADS_PATH,
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

# geckodriver debe ser agregado al path del sistema para que pueda ser usado
# ROUTE TO LOG FILE
LOG_FILE = "../test/test.log"

URL0 = "https://portalcf.cloud.afip.gob.ar/portal/app/index-compat.html"

URL1 = "https://portalcf.cloud.afip.gob.ar/portal/app/"  # ADDED 21/03/2022
# original URL1 = "https://portalcf.cloud.afip.gob.ar/portal/app/index-compat.html"
URL2 = "https://auth.afip.gob.ar/contribuyente_/loginClave.xhtml"
# URL ESTATICA DE AFIP
URL3 = "https://portalcf.cloud.afip.gob.ar/portal/app/mis-servicios"
# URL nuevo fecha 3/2/2022

URL_LOGIN_AFIP = "https://auth.afip.gob.ar/contribuyente_/login.xhtml"

# XPATHS DE AFIP
XPATH_REINGRESO = "//*[@id='aIngresarDeNuevo']"
XPATH_CUIT_AFIP = "//*[@id='F1:username']"
XPATH_CUIT_INVALIDO = "//*[@id='F1:msg']"
XPATH_PWD_AFIP = "//*[@id='F1:password']"
XPATH_CCMA = "/html/body/main/section[1]/div/div[24]/div/div/div"  # inutil
CLASS_CCMA = "bold"  # inutil
NAME_CCMA = 'CCMA - CUENTA CORRIENTE DE CONTRIBUYENTES MONOTRIBUTISTAS Y AUTONOMOS'
NAME_COMPROBANTES = "Comprobantes en línea"
NAME_MONOTRIBUTO_LISTA = "Monotributo"
NAME_MONOTRIBUTO = """AFIP
Monotributo
Adhesión y/o empadronamiento al monotributo"""
NAME_MIS_COM = "Mis Comprobantes"
XPATH_MONOTRIBUTO2 = "/html/body/div[4]/div/div/div[2]/div/form/div/div[2]/div[2]/div[1]/ul/li[7]/a/p"
XPATH_CAL_DEUDA = "/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/form/table/tbody/tr[4]/td/div/input[3]"
XPATH_BODY_DEUDA = "/html/body/table[2]/tbody/tr[2]/td[2]/form/table[1]/tbody"
XPATH_MONOTRIBUTO = "/html/body/main/section[1]/div/div[14]/div/div/div"
# original XPATH_CAJAS_AFIP = "/html/body/main/section[2]/div/div[*]"
XPATH_CAJAS_AFIP = "/html/body/div/div/main/div[2]/section[2]/div/div/div[*]/div"  # added 21/03/2022
XPATH_CAJAS_NUEVO_12_2022="/html/body/div/div/main/div/section/div/div[3]/div[*]/a"
XPATH_CONSTANCIAS = "//*[@id='menuLateral']/li[4]/a"
XPATH_PAGOS = "//*[@id='menuLateral']/li[2]/a"
XPATH_BTNS_MONOTRIBUTO = "//*[@id='aBtn1']"
XPATH_CAJAS_TIPO_PAGO_OTROS = "/html/body/main/section/div/div/form/div[3]/div[2]/div[2]/div[*]/div[*]/img"
XPATH_VEP_GENERAR = "//*[@id='btnPagar']"
XPATH_TIPO_CONSTANCIA = "/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr/td/table/tbody/tr[2]/td[2]/select"
XPATH_CONSTANCIAS_LISTA = "/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr/td/table/tbody/tr[2]/td[2]/select/option[*]"
# XPATH_OPTION_MONOTRIBUTO = "/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr/td/table/tbody/tr[2]/td[2]/select/option[3]"
NAME_LISTA_OPTION = "Opción - Monotributo"
XPATH_OPTION_CONTINUAR = "/html/body/table[2]/tbody/tr[2]/td/form/table/tbody/tr/td/table/tbody/tr[3]/td/input[2]"
XPATH_VER_CONSTANCIA = "//*[@id='bBtn1']"
XPATH_CONSTANCIA_INSC = "/html/body/table[2]/tbody/tr[1]"
# XPATH_ACTIVIDAD_CONSTANCIA = "/html/body/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[16]/td/table/tbody/tr"
XPATH_ACTIVIDAD_CONSTANCIA = "/html/body/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[*]/td/table/tbody/tr"
XPATH_DIRECCION_CONSTANCIA1 = "/html/body/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[7]/td/table/tbody/tr[3]"
XPATH_DIRECCION_CONSTANCIA2 = "/html/body/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[7]/td/table/tbody/tr[4]/td"
XPATH_COMPROBANTES = "/html/body/main/section[1]/div/div[8]/div/div/div"  # inutil
XPATH_LISTA_URL_2 = "/html/body/div[4]/div/div/div[2]/div/form/div/div[2]/div[2]/div[*]/ul/li[*]/a"
xxxx = "/html/body/div[4]/div/div/div[2]/div/form/div/div[2]/div[2]/div[1]/ul/li[7]/a"
XPATH_COMPROBANTES_REPRESENTAR = "//*[@id='contenido']/form/table/tbody/tr[4]/td"
XPATH_COMPROBANTES_CONSULTAS = "//*[@id='btn_consultas']"
XPATH_COMPROBANTES_CON_FROM = "//*[@id='fed']"
XPATH_COMPROBANTES_CON_TO = "//*[@id='feh']"
XPATH_FACTURA_C = "/html/body/div[2]/form/div/div/table/tbody/tr[4]/td/select/option[10]"
XPATH_PTO_VENTA = "/html/body/div[2]/form/div/div/table/tbody/tr[5]/td/select/option[2]"
XPATH_BUSCAR_FACT_C = "/html/body/div[2]/table/tbody/tr/td/input[2]"
XPATH_FACTURA_C_VER = ".//html/body/div[2]/div[3]/div/table/tbody/tr[*]/td[7]/input"
XPATH_RECIBO_C = "/html/body/div[2]/form/div/div/table/tbody/tr[4]/td/select/option[13]"
XPATH_CONSULTA_SIFERE = "//*[@id='servicesContainer']/div[29]"
XPATH_CAT = "/html/body/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[10]/td/table/tbody/tr/td[2]/table/tbody/tr/td/font[2]"
XPATH_MIS_COMPROBANTES = "/html/body/main/section[1]/div/div[25]/div/div/div/div[2]/h4"
XPATH_MISC_EMITIDOS = "//*[@id='btnEmitidos']/div[2]/p"
XPATH_MISC_RECIBIDOS = "//*[@id='btnRecibidos']/div[2]/h3"
XPATH_MISC_RANGO_FECHA = "//*[@id='fechaEmision']"
XPATH_MISC_BUSCAR = "//*[@id='buscarComprobantes']"
NAME_BASE_MISC_EMITIDOS = "Mis Comprobantes Emitidos - CUIT"
NAME_BASE_MISC_RECIBIDOS = "Mis Comprobantes Recibidos - CUIT"
XPATH_MISC_DCSV = "//*[@id='tablaDataTables_wrapper']/div[1]/div[1]/div/button[1]/span"
NAME_ACEPTACION_BIOMETRICA = "Aceptación de Datos Biométricos"
XPATH_DATOS_ACEPTADOS = "/html/body/div/div/main/section/div/div[2]/div/div[1]/div/div/div[2]/p"
NAME_ACEPTADO = "¡Tus datos biométricos se encuentran aceptados!"
NAME_SIS_REGISTRAL = "Sistema registral"
XPATH_RUT = "//*[@id='infoContribuyente']/div[*]/div/div/div[2]"
#XPATH_RUT = "//*[@id='infoContribuyente']/div[*]/div/div"
NAME_RUT = "Registro Único Tributario"
XPATH_GROUP_URL2 = "/html/body/div[4]/div/div/div[2]/div/form/div/div[2]/div[2]"
ID_GROUP_URL1 = "servicesContainer"
XPATH_CAPCHAT = "/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]"
XPATH_DISTRACCION = "/html/body/nav/div/div/div[2]/div/ul/li[1]/a"
XPATH_BUTONS_MONOTRIBUTO = "/html/body/form/main/section/div/div/div/div[*]/div/div/div[3]/button"
NAME_RECATEGORIZAR = "Recategorizarme"
XPATH_FACTURAS_EMITIDAS_REC = "/html/body/form/main/section[2]/div/div/div/div[1]/div/div/div[2]/table[1]/tbody/tr[2]"
XPATH_CONT_RECAT = "/html/body/form/main/section[2]/div/div/div/div[2]/div/div/div[2]/div[2]/input[1]"
XPATH_RECAT_MONTO_INPUT = "/html/body/form/main/section[2]/div/div/div/div/div/div/div[2]/div[1]/div[1]/div/input"
XPATH_RECAT_RADIO_SI_1 = "/html/body/form/main/section[2]/div/div/div/div/div/div/div[2]/div[1]/div[2]/div/input[1]"
XPATH_RECAT_RADIO_NO_1 = "/html/body/form/main/section[2]/div/div/div/div/div/div/div[2]/div[1]/div[2]/div/input[2]"
XPATH_EEC = "//*[@id='txtEnergia1']"
XPATH_SUP_AFEC = "//*[@id='txtSup1']"
XPATH_ALQ_RADIO_SI = "//*[@id='collapseMoreInfo1']/div[3]/div/input[1]"
XPATH_ALQ_RADIO_NO = "//*[@id='collapseMoreInfo1']/div[3]/div/input[2]"
XPATH_ALQ_CORRES = "//*[@id='txtAlquiler1']"
XPATH_SELECT_INM = "//*[@id='selCantAlquiler']"
XPATH_CUIT_LOCADOR = "/html/body/form/main/section[2]/div/div/div/div/div/div/div[2]/div[1]/div[3]/div[4]/div[3]/div[*]/div[1]/input"
XPATH_RECAT_CONT_1 = "/html/body/form/main/section[2]/div/div/div/div/div/div/div[2]/div[2]/input[2]"
XPATH_RECAT_CAT_NUEVA = "/html/body/form/main/section[2]/div/div/div/div/div/div/div[2]/h2/strong"
XPATH_RECAT_RESUMEN = "/html/body/form/main/section[2]/div/div/div/div/div/div/div[2]/table"
XPATH_RECAT_CONFIRMAR_CAT = "/html/body/form/main/section[2]/div/div/div/div/div/div/div[2]/div/input[2]"
XPATH_BUTONS_MODIFICAR = "/html/body/form/main/section/div/div/div/div[*]/div/div/div[3]/button"
NAME_MODIFICAR = "MODIFICAR MIS DATOS"
NAME_BAJA = "DAR DE BAJA"
XPATH_MODIFICAR_MIS_DATOS = "//*[@id='bBtn1']"
XPATH_RADIO_MODIF_COOP = "/html/body/form/main/section[2]/div/div/div/div[2]/div[1]/label/input"
XPATH_RADIO_MODIF_INDEP = "/html/body/form/main/section[2]/div/div/div/div[1]/div[1]/label/input"
XPATH_RADIO_MODIF_PROM = "/html/body/form/main/section[2]/div/div/div/div[3]/div[1]/div[1]/label/input"
XPATH_MOD_BUTON_SIGU = "//*[@id='btnSiguiente']"
XPATH_MOD_RADIO_STP2_ACTUAL = "//*[@id='divPeriodos']/div[1]/div/label/input"
XPATH_MOD_RADIO_STP2_PROX = "//*[@id='divPeriodos2']/div/label/input"
XPATH_MOD_FORM_STP2_FACT_ANUAL = "//*[@id='txtIIBB1']"
XPATH_MOD_FORM_STP2_RADIO_LOCAL_NO = "//*[@id='divLocal']/div/input[2]"
XPATH_MOD_FORM_STP2_RADIO_LOCAL_SI = "//*[@id='divLocal']/div/input[1]"
XPATH_MOD_STP2_ENER_ANUAL = "//*[@id='txtEnergia1']"
XPATH_MOD_STP2_RADIO_LOC_ALQ_SI = "//*[@id='collapseMoreInfo1']/div[2]/div/input[1]"
XPATH_MOD_STP2_RADIO_LOC_ALQ_NO = "//*[@id='collapseMoreInfo1']/div[2]/div/input[2]"
XPATH_MOD_STP2_FORM_MONTO_ALQ = "//*[@id='txtAlquiler1']"
XPATH_MOD_STP2_FORM_SUP_AFEC = "//*[@id='txtSup1']"
XPATH_MOD_BUTON_SIGU_STP2 = "//*[@id='btnSiguiente']"
XPATH_MOD_RADIO_STP3_ACT = "//*[@id='divSeleccionJubilacion']/div[1]/div[1]/label/input"
XPATH_MOD_RADIO_STP3_DEP = "//*[@id='divSeleccionJubilacion']/div[2]/div[1]/label/input"
XPATH_MOD_BUTON_CAM_EMP = "//*[@id='btnCambiarEmpleador']"
XPATH_MOD_FORM_CAM_EMP = "//*[@id='txtCuitEmpleador']"
XPATH_MOD_RADIO_STP3_JUBILADO = "//*[@id='divSeleccionJubilacion']/div[4]/div[1]/label/input"
XPATH_MOD_RADIO_STP3_LEY_24241 = "//*[@id='collapse-jub']/div[1]/div/label/input"
XPATH_MOD_RADIO_STP3_LEY_180388 = "//*[@id='collapse-jub']/div[2]/div/label/input"
XPATH_MOD_RADIO_STP3_CAJA = "//*[@id='divSeleccionJubilacion']/div[6]/div[1]/label/input"
XPATH_MOD_FORM_STP3_CAJ_CUIT = "//*[@id='txtCuitCaja']"
XPATH_MOD_RADIO_STP3_LOCADOR = "//*[@id='divSeleccionJubilacion']/div[8]/div[1]/label/input"
XPATH_MOD_BUTON_SIGU_STP3 = "//*[@id='btnSiguiente']"
XPATH_MOD_STP4_YA_TIENE = "/html/body/form/main/section[2]/div/div/div/h4"
XPATH_MOD_STP4 = "//*[@id='divContentPlaceHolder1']/p[1]"
XPATH_MOD_STP4_CONT = "//*[@id='btnSiguiente']"
XPATH_MOD_STP4_OS1 = "/html/body/form/main/section[2]/div/div/div/div[1]/div[1]/div[1]/div/a/span"
XPATH_MOD_STP4_OS2 = "/html/body/form/main/section[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div/input"
XPATH_MOD_STP4_RADIO_APORTE_N = "//*[@id='divSeleccionObraSocial']/div[4]/div/label/strong"
XPATH_MOD_STP4_RADIO_APORTE_S = "//*[@id='divSeleccionObraSocial']/div[2]/div/label/strong"
XPATH_MOD_STP4_CUIL_CONY = "//*[@id='txtCuilConyuge']"
XPATH_MOD_STP4_BTN_AGRE_CONY = "//*[@id='btnAgregarConyuge']"
XPATH_MOD_STP4_FORM_CUIL_FAM = "//*[@id='txtCuilFamiliar']"
XPATH_MOD_STP4_SELECT_AGRE_FAM = "/html/body/form/main/section[2]/div/div/div/div[1]/div[5]/div/div[3]/div[2]/select"
XPATH_MOD_STP4_BTN_AGRE_FAM = "//*[@id='btnAgregarFamiliar']"
XPATH_MOD_STP4_CHKBX_SIPA = "//*[@id='chkSipa']"
XPATH_MOD_STP4_CONFIRMAR = "//*[@id='btnSiguiente']"
XPATH_MOD_STP5_RESUMEN = "//*[@id='divContentPlaceHolder1']/div[2]"

XPATH_CALENDARIO_BAJA = "//*[@id='datePickerPeriodo']"
DICT_XPATH_BAJA = {
    "CESE": "/html/body/form/main/section/div/div/div/div[1]/div/div/div[2]/div[1]/div[1]/label/input",
    "RENUNCIA": "/html/body/form/main/section/div/div/div/div[1]/div/div/div[2]/div[2]/div[1]/label/input",
    "EXCLUSION": "/html/body/form/main/section/div/div/div/div[1]/div/div/div[2]/div[3]/div[1]/label/input"
}
XPATH_BAJA_MON_CONTI = "//*[@id='btnContinuar']"
XPATH_BAJA_GO_RUT = "//*[@id='btnBajaMonotributo']"
XPATH_BAJA_CONFIRMAR_IMP = "//*[@id='btnPasoSiguiente']"

# ################ XPATHS DE SIFERE #################

# URL consulta sifere
url_consulta_sif = "https://auth.afip.gob.ar/contribuyente_/login.xhtml?action=SYSTEM&system=comarb_sifereweb_consultas"
NAME_SIFERE = "SIFERE WEB - Consultas"
XPATH_JURISD_SIFERE = "//*[@id='contentMarg']/table/tbody/tr/td[3]"
XPATH_LISTA_CM03_ACTIONS = "//*[@id='gridbox']/div[2]/table/tbody/tr[2]/td[1]/a[*]"
XPATH_CM03_FILTRO_ANTICIPO = "//*[@id='gridbox']/div[1]/table/tbody/tr[3]/td[2]/div/input"
XPATH_SIFERE_DDJJ_CUIT = "//*[@id='cuit']"
XPATH_SIFERE_DDJJ_CUIT_SELEC = "//*[@id='sfrDdjjForm']/fieldset/div/table/tbody/tr[2]/td[5]/input"
XPATH_SIFERE_AUX_WIN = "//*[@id='sfrDdjjForm']/fieldset/div/table/tbody/tr[2]/td[5]/input[1]"
XPATH_LISTA_DDJJ_SIFERE = "//*[@id='fondo_contenido']/div[4]/div/div[2]/ul/li[1]/a"
XPATH_CM03_MEDIOS_PAGO = "//*[@id='content']/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div/a[*]"
XPATH_CMO3_VEP_JURISD = "//*[@id='gridbox']/div[2]/table/tbody/tr[*]/td[6]/a/i"
XPATH_CM03_ACTUALIZAR = "//*[@id='dj']/input[6]"
XPATH_CM03_VEP_TEXT_JUR = "//*[@id='gridbox']/div[2]/table/tbody/tr[*]/td[2]"
XPATH_POP_JURIS = "//*[@id='jurisdiccionCombo']"
XPATH_CM03_VEP_ACTIONS = "//*[@id='gridbox']/div[2]/table/tbody/tr[*]/td[6]/a/i"

CLASS_NAME_TREE = "standartTreeRow"
XPATH_JURISD_NAME = "//*[@id='gridbox']/div[2]/table/tbody/tr[*]/td[1]"
XPATH_JURISD_MONTO = "//*[@id='gridbox']/div[2]/table/tbody/tr[*]/td[7]"
IFRAME_DDJJ_SIFERE = "/html/body/div[6]/div/div[1]/div/div/table/tbody/tr/td[3]/div/div[2]/div[1]/iframe"
XPATH_ELIMINAR_DDJJ_AUX = "//*[@id='gridbox']/div[2]/table/tbody/tr[2]/td[1]/a[2]/i"

# COMBOS X_PATHS
# La combinación para CCMA debe tener el siguiente orden:
# (XPATH_USERNAME, X_PATH_PASSWORD, XPATH_CCMA, XPATH_CALCULO_DEUDA, XPATH_BODY_DEUDA)
C_XPATHS_CCMA = (XPATH_CUIT_AFIP, XPATH_PWD_AFIP, XPATH_CCMA, XPATH_CAL_DEUDA, XPATH_BODY_DEUDA)
# La combinación para el login debe estar en el siguiente orden: (XPATH_CUIT_AFIP, XPATH_PWD_AFIP)
C_XPATHS_LOGIN = (XPATH_CUIT_AFIP, XPATH_PWD_AFIP)

CLASS_TREE = "standartTreeRow"
NAME_TREE_ACTIVIDADES = "Datos de Actividades"
XPATH_IFRAME = "//*[@id='parentId']/div/div[1]/div/div/table/tbody/tr/td[3]/div/div[2]/div[1]/iframe"
XPATH_ALERTA = "/html/body/div[1]/div/table/tbody/tr/td[1]/img"
XPATH_EDITAR_MONTOS = "//*[@id='contentMarg']/input"
XPATH_TOTAL_MONTO_IMPONIBLE = "//*[@id='montoart2']"
XPATH_MODIFICAR_MONTOS = " //*[@id='datos']/form/div[3]/input[2]"
XPATH_ACTUALIZAR_DEDUCCION = "//*[@id='parametrosForm:refreshDJ']/span"
XPATH_CONFIRMAR_DEDUCCIONES = "//*[@id='j_idt37']"
XPATH_INCLUIR_DEDUCCIONES = "//*[@id='parametrosForm:cerrarDj']/span"
XPATH_CERRAR_DEDUCCION = "//span[contains(.,'Cerrar')]"
XPATH_FRAME_CERRAR = "/html/body/div[13]/div[2]/iframe"
XPATH_BASE_IMPOSIBLE = "//*[@id='ingresosgravados']"
XPATH_NO_GRAVADOS = "//*[@id='ingresosnogravados']"
XPATH_INGRESOS_EXENTOS = "//*[@id='ingresosexentos']"


# XPATH_ACTUALIZAR_INGRESOS = "//*[@id='mod']"
XPATH_ACTUALIZAR_INGRESOS = "//*[@id='actualizar_ingresos']"

# XPATH_TILDE_ACTIVIDADES = "//*[@id='contentMarg']/h2[1]/span/a/i"
XPATH_TILDE_ACTIVIDADES = "/html/body/div[1]/div/table/tbody/tr/td[1]/i"

# XPATH_INPUT_MONTO_SALDO_FAVOR = "//*[@id='contentMarg']/div[1]/form/input[4]"
XPATH_INPUT_MONTO_SALDO_FAVOR = "/html/body/div/div[2]/form/fieldset/div/div[3]/input"

# XPATH_APELLIDO_DDJJ = "//*[@id='contentMarg']/div[2]/form/input[1]"
XPATH_APELLIDO_DDJJ = "/html/body/div[1]/form/fieldset/div[1]/input"

# XPATH_NOMBRE_DDJJ = "//*[@id='contentMarg']/div[2]/form/input[2]"
XPATH_NOMBRE_DDJJ = "/html/body/div[1]/form/fieldset/div[2]/input"

# XPATH_MAIL_DDJJ = "//*[@id='contentMarg']/div[2]/form/input[3]"
XPATH_MAIL_DDJJ = "/html/body/div[1]/form/fieldset/div[3]/input"

# NUMERO_DOCUMENTO = "/html/body/div[1]/div[2]/form/input[4]"
NUMERO_DOCUMENTO = "/html/body/div[1]/form/fieldset/div[6]/input"

# XPATH_XLS = "//*[@id='total']/a/img"
XPATH_XLS = "/html/body/div/form/input[2]"

# XPATH_CERRAR_DDJJ = "/html/body/div/form/input"
XPATH_CERRAR_DDJJ = "//*[@id='cerrar_dj_cm03']"

# XPATH_FILTRO_PRESENTAR = "/html/body/div[2]/div[2]/div[2]/div[1]/table/tbody/tr[3]/td[2]/div/input"
XPATH_FILTRO_PRESENTAR = "/html/body/div[1]/div[2]/div[2]/div[1]/table/tbody/tr[3]/td[2]/div/input"

# XPATH_SIFERE_DDJJ_NUEVA = "//a[contains(text(),'NUEVA DDJJ MENSUAL')]"
XPATH_SIFERE_DDJJ_NUEVA = "/html/body/section[3]/div/div/div[2]/a/div/div[1]/h6"

# XPATH_SIFERE_DDJJ_CREAR = "//input[@value=' Crear nueva DDJJ ']"
XPATH_SIFERE_DDJJ_CREAR = "/html/body/div/div[2]/div/form/div/table/tbody/tr/td[3]/input"

XPATH_ACTIVIDADES_JURISDICCION = "//*[@id='gridbox']/div[2]/table/tbody/tr[*]/td[3]"
XPATH_EDITAR_ACT_JURIS = "//*[@id='debitos']/input[6]"
XPATH_EDITAR_ACT_JURIS_2 = "//*[@id='editar_act_jur']"
XPATH_EDITAR_ALICUOTA = "//*[@id='alicuota']"
XPATH_CLOSE_ALICUOTA = "/html/body/div[11]/div/div[4]/div[7]"
XPATH_SELECT_ANIO_SALDO_FAVOR = "//*[@id='anio']"
XPATH_SELECT_MES_SALDO_FAVOR = "//*[@id='mes']"
SELECT_TITULAR = "//*[@id='caracter']"
SELECT_TIPO_DOCUMENTO = "//*[@id='tipodocumento']"
NAME_SELECT = "CUIT/CUIL/CDI"

XPATH_SIFERE_DDJJ_ANIO = "//select[@id='anio']"
XPATH_SIFERE_DDJJ_MES = "//select[@id='mes']"





STATUS_OK = 0
STATUS_FAIL = 1
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
    "XPATH_MISC_DCSV": "//*[@id='tablaDataTables_wrapper']/div[1]/div[1]/div/button[1]/span"
}
inv_xpath = {}
for k, v in d_xpath.items():
    #print(k)
    inv_xpath[v] = k
