import re
import base64
from os import listdir, remove
from os.path import join, exists
from anfler_base.anfler_baseclass import BaseClass, log_prod
from anfler_afip.anfler_login import Login
from anfler.util.helper import dpath
from selenium.common.exceptions import SessionNotCreatedException, NoSuchWindowException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from anfler.util.msg import message as msg
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from anfler_afip.settings import *
from decimal import Decimal


class SifereDDJJ(BaseClass):

    def __init__(self, message, browser: str = "chrome", t_s: float = 0.5,
                 options: bool = True, *args, **kwargs):
        super(SifereDDJJ, self).__init__()
        log_prod.info("INSTANCING SIFERECONSULTAS CLASS")
        self.data = self.validate_message(message)
        cuit, pwd = self.extract_cuit_pwd(self.data)
        self.cuit, self.pwd = self.validate(cuit, pwd)
        self._id = self.data["id"]
        self.browser = dpath(self.config, "scrapper.afip.Sifereddjj.browser", browser)
        self.t_s = dpath(self.config, "scrapper.afip.Sifereddjj.t_s", t_s)
        self.options = dpath(self.config, "scrapper.afip.Sifereddjj.options", options)
        self.headless = dpath(self.config, "scrapper.afip.Sifereddjj.headless", True)

    def run(self, t_s: float = 1, t_o: float = None, headless: bool = None, c_d=False):
        log_prod.info("START BROWSER TO SIFERE")
        try:
            self.browser = Login(self.cuit,
                                 self.pwd,
                                 browser=self.browser,
                                 t_o=t_o, id_=self._id,
                                 change_dir=c_d).run(C_XPATHS_LOGIN,
                                              t_s=t_s,
                                              options=self.options,
                                              headless=headless)
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            wait_ = WebDriverWait(self.browser, 60)
            actual = self.browser.current_window_handle
            if self.browser.current_url == URL1 or self.browser.current_url == URL0:
                log_prod.debug("=======================URL 1=====================")
                # wait_.until(EC.element_to_be_clickable((By.ID, ID_GROUP_URL1)))
                time.sleep(5)
                self.force_find_xpath(browser=self.browser, xpath=XPATH_CAJAS_AFIP, max_r=30,
                                      t_s=t_s, group=True, name="Convenio Multilateral – SIFERE WEB - DDJJ")
            elif self.browser.current_url == URL2:
                log_prod.debug("=======================URL 2=====================")
                wait_.until(EC.element_to_be_clickable((By.XPATH, XPATH_GROUP_URL2)))
                self.force_find_xpath(self.browser, XPATH_LISTA_URL_2, t_s=t_s, click=True,
                                      group=True, name="Convenio Multilateral – SIFERE WEB - DDJJ")

            elif self.browser.current_url == URL3:
                log_prod.debug(f"job= {self._id} |=======================URL 3=====================")
                print('Estamos en URL3')
                time.sleep(10)
                search = self.force_find_xpath(self.browser,
                                               xpath=XPATH_CAJAS_NUEVO_12_2022,
                                               t_s=t_s,
                                               click=False,
                                               group=True,
                                               name="Convenio Multilateral – SIFERE WEB - DDJJ" )
                self.browser.execute_script("arguments[0].scrollIntoView(true);", search)
                time.sleep(1)
                search.click()

                if isinstance(search, AssertionError):
                    raise search

            else:
                raise NoSuchWindowException("Se accedio a una ruta desconocida")
            wait_.until(EC.number_of_windows_to_be(2))
            ambas = self.browser.window_handles
            self.browser.close()
            for x in ambas:
                if x != actual:
                    self.browser.switch_to.window(x)
            return self.browser
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def select_cuit(self,):
        cuit_to_vep = str(self.data["payload"]["cuit_to_vep"])
        s = self.wait_and_go(xpath=XPATH_SIFERE_DDJJ_CUIT, click=False)
        s = Select(s)
        s.select_by_visible_text(str(cuit_to_vep))
        self.wait_and_go(XPATH_SIFERE_DDJJ_CUIT_SELEC)
        aux = self.browser.find_elements_by_xpath(XPATH_SIFERE_AUX_WIN)
        if len(aux) > 0:
            aux[0].click()

    def lista_cm03(self, search=False, what=None, click=True):
        # self.wait_and_go(xpath=XPATH_LISTA_DDJJ_SIFERE, click=click)
        time.sleep(5)
        self.browser.get("https://sifereweb.comarb.gob.ar/sifereweb/MostrarListaDDJJController.do")
        if search:
            return self.wait_and_go(xpath=what, click=click)

    def lista_cm05(self, search=False, what=None, click=True):
        XPATH_LISTA_CM05_SIFERE = "/html/body/div[6]/div/div[2]/div/ul/li[1]/a"
        self.wait_and_go(xpath=XPATH_LISTA_CM05_SIFERE)
        if search:
            return self.wait_and_go(xpath=what, click=click)

    def vep(self, t_s: float = None, t_o: float = None, headless: bool = None):
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.Sifereddjj.vepcm03.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.Sifereddjj.vepcm03.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.Sifereddjj.vepcm03.headless", headless)
            self.run(t_s=t_s, headless=headless, t_o=t_o, c_d=True)
            self.select_cuit()

            filtro = self.lista_cm03(search=True, what=XPATH_CM03_FILTRO_ANTICIPO, click=False)
            anticipo = str(self.data["payload"]["anticipo"])
            filtro.send_keys(anticipo)
            time.sleep(5)

            acciones = self.browser.find_elements_by_xpath(XPATH_LISTA_CM03_ACTIONS)
            # print(acciones)
            accion_vep = "Generar pago de DDJJ"
            VEP_FINDED = False
            for x in acciones:
                aux = x.get_attribute("title")
                if aux.upper() == accion_vep.upper():
                    VEP_FINDED = True
                    x.click()
                    wait = WebDriverWait(self.browser, self.t_o)
                    wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_CMO3_VEP_JURISD)))
                    time.sleep(3)
                    names = self.browser.find_elements_by_xpath(XPATH_CM03_VEP_TEXT_JUR)
                    jurisd_recorridas = list()
                    total_jurisdicciones = [x.text for x in names]
                    for x in range(len(total_jurisdicciones)):
                        time.sleep(5)
                        acts = self.browser.find_elements_by_xpath(XPATH_CM03_VEP_ACTIONS)
                        acts[x].click()
                        aux_text = self.force_find_xpath(self.browser, xpath=XPATH_POP_JURIS, click=False)
                        aux_text = aux_text.text
                        if aux_text not in jurisd_recorridas:
                            self.wait_and_go(XPATH_CM03_ACTUALIZAR)
                            jurisd_recorridas.append(aux_text)
                    log_prod.info(f"Jurisdicciones recorridas: {str(jurisd_recorridas)}")
                    medio_pago = self.data["payload"]["medio_de_pago"].upper()
                    patron = re.compile(medio_pago)
                    medios_disponibles = self.browser.find_elements_by_xpath(XPATH_CM03_MEDIOS_PAGO)
                    name_dispon = list()
                    for x in medios_disponibles:
                        aux = x.get_attribute("onclick")
                        aux = aux.split(",")[1].replace(");", "")
                        name_dispon.append(aux.replace("'", ""))
                        if re.search(patron, aux.upper()):
                            time.sleep(5)
                            x.click()
                            time.sleep(1)
                            c = self.browser.switch_to.alert
                            c.accept()
                            XPATH_CM03_VEP_DESCARGA = "//*[@id='gridbox']/div[2]/table/tbody/tr[2]/td[1]/a/i"
                            self.wait_and_go(xpath=XPATH_CM03_VEP_DESCARGA, click=True)
                            time.sleep(5)
                            tmp = "/tmp/"
                            file = "VolantePagoVEP"
                            patron = re.compile(file.upper())
                            FINDED = False
                            for x in listdir(join(tmp, self._id)):
                                if re.search(patron, x.upper()):
                                    FINDED = True
                                    with open(join(tmp, self._id, x), "rb") as f:
                                        coded = base64.b64encode(f.read())
                                        remove(join(tmp, self._id, x))
                            if not FINDED:
                                raise FileNotFoundError("No se pudo encontrar el comprobante de VEP en descargas")
                            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                                             payload={"resumen": str(coded)})
                            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
                            self.logout()
                            log_prod.info(f"job= {self._id}|END OF PROCESS")
                            return response
                    if medio_pago not in name_dispon:
                        raise KeyError(f"El medio de pago {medio_pago} no esta disponible, opciones: {name_dispon}")
            if not VEP_FINDED:
                raise KeyError(f"No se encontro opcion para generar VEP en el periodo seleccionado")
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def descarga_cm03(self, t_s: float = None, t_o: float = None, headless: bool = None):
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.Sifereddjj.descarga_cm03.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.Sifereddjj.descarga_cm03.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.Sifereddjj.descarga_cm03.headless", headless)
            self.run(t_s=t_s, headless=headless, t_o=t_o, c_d=True)
            self.select_cuit()
            filtro = self.lista_cm03(search=True, what=XPATH_CM03_FILTRO_ANTICIPO, click=False)
            anticipo = str(self.data["payload"]["anticipo"])
            filtro.send_keys(anticipo)
            time.sleep(2)
            acciones = self.browser.find_elements_by_xpath(XPATH_LISTA_CM03_ACTIONS)
            accion = "Reporte de DDJJ"
            REPORTE_FINDED = False
            for x in acciones:
                aux = x.get_attribute("title")
                if aux.upper() == accion.upper():
                    REPORTE_FINDED = True
                    name = "DDJJ_Mensual_"
                    sfx = x.get_attribute("href").split("=")[-1]
                    name = name + str(sfx)
                    x.click()
                    time.sleep(10)
                    tmp = "/tmp/"
                    patron = re.compile(name.upper())
                    download = None
                    for x in listdir(join(tmp, str(self._id))):
                        if re.search(patron, x.upper()):
                            with open(join(tmp, str(self._id), x), "rb") as f:
                                download = base64.b64encode(f.read())
                            remove(join(tmp, str(self._id), x))
                    if not download:
                        log_prod.error("El resumen descargado no pude ser localizado")
                        raise FileNotFoundError("El resumen descargado no pude ser localizado")
                    response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                                     payload={"pdf cm03 descargado": str(download)})
                    response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
                    self.logout()
                    log_prod.info(f"job= {self._id}|END OF PROCESS")
                    return response
            if not REPORTE_FINDED:
                raise FileNotFoundError(f"El reporte para el anticipo {anticipo} no fue encontrado")
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def descarga_cm05(self, t_s: float = None, t_o: float = None, headless: bool = None):
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.Sifereddjj.descarga_cm05.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.Sifereddjj.descarga_cm05.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.Sifereddjj.descarga_cm05.headless", headless)
            self.run(t_s=t_s, headless=headless, t_o=t_o, c_d=True)
            self.select_cuit()
            filtro = self.lista_cm05(search=True, what=XPATH_CM03_FILTRO_ANTICIPO, click=False)
            anticipo = str(self.data["payload"]["anticipo"])
            filtro.send_keys(anticipo)
            time.sleep(2)
            acciones = self.browser.find_elements_by_xpath(XPATH_LISTA_CM03_ACTIONS)
            accion = "Reporte de DDJJ"
            REPORTE_FINDED = False
            for x in acciones:
                aux = x.get_attribute("title")
                if aux.upper() == accion.upper():
                    REPORTE_FINDED = True
                    name = "DDJJ_anual_"
                    sfx = x.get_attribute("href").split("=")[-1]
                    name = name + str(sfx)
                    x.click()
                    time.sleep(10)
                    tmp = "/tmp/"
                    patron = re.compile(name.upper())
                    download = None
                    for x in listdir(join(tmp, str(self._id))):
                        if re.search(patron, x.upper()):
                            with open(join(tmp, str(self._id), x), "rb") as f:
                                download = base64.b64encode(f.read())
                            remove(join(tmp, str(self._id), x))
                    if not download:
                        log_prod.error("El resumen descargado no pude ser localizado")
                        raise FileNotFoundError("El resumen descargado no pude ser localizado")
                    response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                                     payload={"pdf cm05 descargado": str(download)})
                    response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
                    self.logout()
                    log_prod.info(f"job= {self._id}|END OF PROCESS")
                    return response
            if not REPORTE_FINDED:
                raise FileNotFoundError(f"El reporte para el anticipo {anticipo} no fue encontrado")
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def search_in_tree(self, class_tree, name):
        trees = self.browser.find_elements_by_class_name(class_tree)
        for x in trees:
            if x.text.upper().replace(" ", "") == name.upper().replace(" ", ""):
                return x
        raise KeyError(f"El objeto {name} no pudo ser encontrado")

    def saldo_favor(self, t_s: float = None, t_o: float = None, headless: bool = None):
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.Sifereddjj.saldo_favor.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.Sifereddjj.saldo_favor.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.Sifereddjj.saldo_favor.headless", headless)
            self.run(t_s=t_s, headless=headless, t_o=t_o, c_d=True)
            self.select_cuit()
            filtro = self.lista_cm03(search=True, what=XPATH_CM03_FILTRO_ANTICIPO, click=False)
            acciones = self.browser.find_elements_by_xpath(XPATH_LISTA_CM03_ACTIONS)
            accion = "Crear DDJJ a partir de copia"
            XPATH_LISTA_CM03_EDITAR = "//*[@id='gridbox']/div[2]/table/tbody/tr[2]/td[1]/a[1]/i"
            REPORTE_FINDED = True
            wait = WebDriverWait(self.browser, 60)
            for x in acciones:
                aux = x.get_attribute("title")
                if aux.upper() == accion.upper():
                    REPORTE_FINDED = False
                    x.click()
                    time.sleep(5)
                    self.wait_and_go(xpath=XPATH_LISTA_CM03_EDITAR)
                    tabla = "//*[@id='gridbox']"
                    f = self.search_in_tree(class_tree=CLASS_NAME_TREE, name="finalizar ddjj")
                    if f is not None:
                        f.click()
                    iframe = self.wait_and_go(xpath=IFRAME_DDJJ_SIFERE, click=False)
                    self.browser.switch_to.frame(iframe)
                    juris_name = self.browser.find_elements_by_xpath(XPATH_JURISD_NAME)
                    juris_monto = self.browser.find_elements_by_xpath(XPATH_JURISD_MONTO)
                    r = list()
                    for k, v in zip(juris_name, juris_monto):
                        r.append(f"{k.text}={v.text}")
                    self.browser.get("https://sifereweb.comarb.gob.ar/sifereweb/MostrarListaDDJJController.do")
                    self.wait_and_go(xpath=XPATH_ELIMINAR_DDJJ_AUX)
                    time.sleep(2)
                    alert = self.browser.switch_to.alert
                    alert.accept()
                    time.sleep(2)
                    self.logout()
                    response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                                     payload={"lista de saldo a favor:": str(r)})
                    response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
                    log_prod.info(f"job= {self._id}|END OF PROCESS")
                    return response
            if not REPORTE_FINDED:
                raise FileNotFoundError(f"El reporte no fue encontrado")
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def coeficientes_unificados_cm05(self, t_s: float = None, t_o: float = None, headless: bool = None):
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.Sifereddjj.coeficientes_unificados_cm05.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.Sifereddjj.coeficientes_unificados_cm05.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.Sifereddjj.coeficientes_unificados_cm05.headless", headless)
            self.run(t_s=t_s, headless=headless, t_o=t_o, c_d=True)
            self.select_cuit()
            anticipo = self.data["payload"]["anticipo"]
            if anticipo is not None:
                filtro = self.lista_cm03(search=True, what=XPATH_CM03_FILTRO_ANTICIPO, click=True)
                filtro.send_keys(anticipo)
            else:
                self.lista_cm03(search=False, click=True)
            time.sleep(5)
            acciones = self.browser.find_elements_by_xpath(XPATH_LISTA_CM03_ACTIONS)
            accion = "Crear DDJJ a partir de copia"
            REPORTE_FINDED = False
            for x in acciones:
                aux = x.get_attribute("title")
                if aux.upper() == accion.upper():
                    REPORTE_FINDED = True
                    x.click()
                    if anticipo is not None:
                        time.sleep(5)
                        n = str(int(anticipo[-1]) + 1)
                        anticipo = anticipo[:-1] + n
                        filtro = self.wait_and_go(xpath=XPATH_CM03_FILTRO_ANTICIPO, click=False)
                        filtro.send_keys(anticipo)
                    time.sleep(5)
                    XPATH_EDITAR_DDJJ = "//*[@id='gridbox']/div[2]/table/tbody/tr[2]/td[1]/a[1]/i"
                    self.wait_and_go(xpath=XPATH_EDITAR_DDJJ, click=True)
                    j = self.search_in_tree(class_tree="standartTreeRow", name="Datos de Jurisdicciones")
                    j.click()
                    frame = "//*[@id='parentId']/div/div[1]/div/div/table/tbody/tr/td[3]/div/div[2]/div[1]/iframe"
                    frame = self.force_find_xpath(self.browser, frame, click=False)
                    self.browser.switch_to.frame(frame)
                    XPATH_TABLA_JURISDICCIONES = "//*[@id='gridbox']"
                    XPATH_DATOS_JURISDICCION = "//*[@id='gridbox']/div[2]/table/tbody/tr[*]"
                    self.wait_and_go(xpath=XPATH_TABLA_JURISDICCIONES, click=False)
                    items = self.find_xpaths(browser=self.browser, xpath=XPATH_DATOS_JURISDICCION, lista=True,
                                             click=False)
                    r = dict()
                    n = 0
                    for x in items:
                        if len(x.text)>0:
                            r[n] = x.text
                            n += 1
                    response = {"Jurisdicción_Domicilio_coeficiente_articulo_14": r}
                    self.browser.get("https://sifereweb.comarb.gob.ar/sifereweb/MostrarListaDDJJController.do")
                    if anticipo is not None:
                        filtro = self.wait_and_go(xpath=XPATH_CM03_FILTRO_ANTICIPO, click=False)
                        filtro.send_keys(anticipo)
                    self.wait_and_go(xpath=XPATH_ELIMINAR_DDJJ_AUX)
                    time.sleep(2)
                    alert = self.browser.switch_to.alert
                    alert.accept()
                    time.sleep(2)
                    response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                                     payload=response)
                    response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
                    log_prod.info(f"job= {self._id}|END OF PROCESS")
                    self.logout()
                    return response
            if not REPORTE_FINDED:
                raise KeyError(f"No se pudo encontrar '{accion}'")
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def go_left(self):
        time.sleep(0.5)
        alerta = self.browser.find_elements_by_xpath(XPATH_ALERTA)
        if len(alerta) > 0:
            indicador = alerta[0].get_attribute("src").split("/")[-1]
            if indicador.upper() == "OK.PNG":
                text = self.wait_and_go(xpath="/html/body/div[1]/div/table/tbody/tr/td[2]", click=False)
                log_prod.warning(f"{text.text}")
            elif indicador.upper() == "ERROR.GIF":
                text = self.wait_and_go(xpath="/html/body/div[1]/div/table/tbody/tr/td[2]", click=False)
                log_prod.error(f"{text.text}")
                response = text.text + " DEBERA REVISAR LA INFORMACIÓN SUMINISTRADA Y ELIMINAR LA DDJJ MANUALMENTE " \
                                       "ANTES DE INTENTAR CARGARLA AUTOMATICAMENTE"
                raise NotImplementedError(response)
            else:
                pass
        self.browser.switch_to.default_content()

    def go_right(self, frame=XPATH_IFRAME, t_s=4):
        # time.sleep(t_s)
        wait = WebDriverWait(self.browser, 60)
        frame = self.wait_and_go(xpath=frame, click=False)
        wait.until(EC.frame_to_be_available_and_switch_to_it(frame), message=f"Esperando frame para cambiar {frame}")
        # self.browser.switch_to.frame(frame)

    def cargar_actividades(self, ):
        actividades = self.search_in_tree(class_tree=CLASS_TREE, name=NAME_TREE_ACTIVIDADES)
        actividades.click()
        self.go_right()
        XPATH_BODY_TABLA_ACTIVIDADES = "/html/body/div/div[1]/div[2]/table/tbody"
        self.wait_and_go(xpath=XPATH_BODY_TABLA_ACTIVIDADES, click=False, what="VISIBLE")
        for actividad in self.data["payload"]["actividades"]:
            tds = self.browser.find_elements_by_tag_name("td")
            if len(tds) > 0:
                for codigo in tds:
                    if codigo.text.upper().strip() == str(actividad["cod_actividad"]):
                        codigo.click()
                        self.wait_and_go(xpath=XPATH_EDITAR_MONTOS)
                        art2 = self.wait_and_go(xpath=XPATH_TOTAL_MONTO_IMPONIBLE, click=False)
                        reg_esp = self.wait_and_go(id_="montoregimenesesp", click=False)
                        ini_act = self.wait_and_go(id_="montoinicioactiv", click=False)
                        clickable_art2 = art2.get_attribute("readonly")
                        clickable_reg_p = reg_esp.get_attribute("readonly")
                        clickable_ini_act = ini_act.get_attribute("readonly")
                        if clickable_art2 != "true": # para cargar base imponible
                            art2.clear()
                            art2.send_keys(str(actividad["monto_imponible"]))
                        elif clickable_reg_p != "true":
                            reg_esp.clear()
                            reg_esp.send_keys(str(actividad["monto_imponible"]))
                        elif clickable_ini_act != "true":
                            ini_act.clear()
                            ini_act.send_keys(str(actividad["monto_imponible"]))
                        self.wait_and_go(xpath=XPATH_MODIFICAR_MONTOS)
                        self.wait_and_go(xpath="/html/body/div/div[2]/div[2]/table/tbody", click=False, what="VISIBLE")
                        break
        return self.browser

    def cargar_deducciones(self):
        wait = WebDriverWait(self.browser, 60)
        deducciones = self.search_in_tree(class_tree="standartTreeRow", name="Carga de Deducciones")
        deducciones.click()
        actualizar = self.browser.find_elements_by_xpath(XPATH_ACTUALIZAR_DEDUCCION)
        while len(actualizar) == 0:
            self.go_left()
            aux = self.search_in_tree(class_tree=CLASS_TREE, name=NAME_TREE_ACTIVIDADES)
            aux.click()
            deducciones = self.search_in_tree(class_tree="standartTreeRow", name="Carga de Deducciones")
            deducciones.click()
            self.go_right()
            actualizar = self.browser.find_elements_by_xpath(XPATH_ACTUALIZAR_DEDUCCION)
        actualizar[0].click()
        self.wait_and_go(xpath=XPATH_CONFIRMAR_DEDUCCIONES, what="VISIBLE")
        XPATH_MENSAJE_INCLUIR = "//*[@id='j_idt137_complete']"
        wait.until_not(EC.visibility_of_element_located((By.XPATH, XPATH_MENSAJE_INCLUIR)))
        time.sleep(4)
        self.wait_and_go(xpath=XPATH_INCLUIR_DEDUCCIONES)
        XPATH_CONFIRMAR_INCLUIR = "//*[@id='j_idt37']"
        self.wait_and_go(xpath=XPATH_CONFIRMAR_INCLUIR, what="VISIBLE")
        self.go_right(frame=XPATH_FRAME_CERRAR)
        self.wait_and_go(xpath=XPATH_CERRAR_DEDUCCION, what="VISIBLE")

    def cargar_actividades_juris(self):
        # juris = self.wait_and_go(xpath="//span[contains(.,'901 CAPITAL FEDERAL')]", click=False)
        self.data["payload"]["jurisdicciones"] = dict(sorted(self.data["payload"]["jurisdicciones"].items()))
        for j, d in self.data["payload"]["jurisdicciones"].items():
            juris = self.search_in_tree(class_tree=CLASS_TREE, name=j)
            accion = ActionChains(self.browser)
            accion.double_click(on_element=juris).perform()
            act_juris = self.search_in_tree(class_tree=CLASS_TREE, name="Actividades por Jurisdicción")
            act_juris.click()
            self.go_right()
            time.sleep(2)
            ingresos = self.wait_and_go(xpath=XPATH_BASE_IMPOSIBLE, click=False)
            ingresos.clear()
            ingresos.send_keys(str(self.data["payload"]["jurisdicciones"][j]["base_imponible"]))
            no_gravados = self.wait_and_go(xpath=XPATH_NO_GRAVADOS, click=False)
            no_gravados.clear()
            no_gravados.send_keys(str(self.data["payload"]["jurisdicciones"][j].get("ingresos_no_gravados", 0)))
            exentos = self.wait_and_go(xpath=XPATH_INGRESOS_EXENTOS, click=False)
            exentos.clear()
            exentos.send_keys(str(self.data["payload"]["jurisdicciones"][j].get("ingresos_exentos", 0)))
            self.wait_and_go(xpath=XPATH_ACTUALIZAR_INGRESOS)
            self.wait_and_go(xpath=XPATH_ACTIVIDADES_JURISDICCION, click=False)
            actividades_declaradas = list(self.data["payload"]["jurisdicciones"][j]["actividades"].keys())
            XPATH_TABLA_ACTIVIDADES_DECL = "/html/body/div[1]/form[3]/div/div[2]/table/tbody"
            self.wait_and_go(xpath="//*[@id='gridbox']/div[2]/table/tbody", click=False, what="VISIBLE")
            for x in actividades_declaradas:
                # time.sleep(2)
                actividades = self.browser.find_elements_by_xpath(XPATH_ACTIVIDADES_JURISDICCION)
                for y in actividades:
                    if y.text.upper() == x.upper():
                        y.click()
                        try:
                            self.wait_and_go(xpath=XPATH_EDITAR_ACT_JURIS_2)
                        except Exception:
                            self.wait_and_go(xpath=XPATH_EDITAR_ACT_JURIS)
                        alicuota = self.data["payload"]["jurisdicciones"][j]["actividades"][x]["alicuota"]
                        self.browser.fullscreen_window()
                        aux = self.wait_and_go(xpath=XPATH_EDITAR_ALICUOTA, click=False)
                        base_imponible = self.wait_and_go(id_="baseimponible", click=False)
                        if not base_imponible.get_attribute("readonly"):
                            base_imponible.clear()
                            base_imponible.send_keys(str(self.data["payload"]["jurisdicciones"][j]["base_imponible"]))
                        if not aux.get_attribute("readonly"):
                            aux.clear()
                            aux.send_keys(str(alicuota)) # + Keys.TAB + Keys.RETURN)
                        mods = self.browser.find_elements_by_id("mod")  # "//*[@id='mod']"
                        tag = self.browser.find_elements_by_tag_name("input")
                        finded = False
                        if len(tag) > 0:
                            act_patron = re.compile("ACTUALIZAR DATOS")
                            for m in tag:
                                if act_patron.search(m.text.upper()):
                                    m.click()
                                    finded = True
                        if len(mods) > 0:
                            act_patron = re.compile("ACTUALIZAR DATOS")
                            for m in mods:
                                if act_patron.search(m.text.upper()):
                                    m.click()
                                    finded = True
                        if not finded:
                            try:
                                self.browser.execute_script("javascript:actualizar(window.document.debitos2)")
                                finded = True
                            except Exception as e:
                                log_prod.error(f"JAVASCRIPT SCRIPT FAILED {str(e)}")
                        name = self.browser.find_elements_by_name("mod")
                        if len(name) > 0:
                            act_patron = re.compile("ACTUALIZAR DATOS")
                            for m in name:
                                if act_patron.search(m.text.upper()):
                                    m.click()
                                    finded = True
                        if not finded:
                            time.sleep(10)
                            accion = ActionChains(self.browser)
                            accion.move_to_element_with_offset(aux,
                                                               xoffset=aux.size["width"] + 50,
                                                               yoffset=aux.size["height"] / 2).click().perform()
                            time.sleep(5)
                            close = self.browser.find_elements_by_xpath(XPATH_CLOSE_ALICUOTA)
                            if len(close) > 0:
                                close[0].click()
                        self.wait_and_go(xpath="//*[@id='gridbox']/div[2]/table/tbody", click=False, what="VISIBLE")
                        break
            self.wait_and_go(xpath=XPATH_TILDE_ACTIVIDADES)
            self.cargar_saldo_favor(j=j)
            self.go_left()
            time.sleep(2)
            juris = self.search_in_tree(class_tree=CLASS_TREE, name=j)
            accion = ActionChains(self.browser)
            accion.double_click(on_element=juris).perform()

    def cargar_saldo_favor(self, j):
        self.go_left()
        time.sleep(4)
        periodos_ant = self.search_in_tree(class_tree="standartTreeRow", name="Saldos a Favor Períodos Anteriores")
        periodos_ant.click()
        self.go_right()
        select_anio = self.wait_and_go(xpath=XPATH_SELECT_ANIO_SALDO_FAVOR, click=False)
        select_anio = Select(select_anio)
        select_mes = self.wait_and_go(xpath=XPATH_SELECT_MES_SALDO_FAVOR, click=False)
        select_mes = Select(select_mes)
        anio = self.data["payload"]["jurisdicciones"][j]["saldo_favor"]["periodo_anio"]
        mes = self.data["payload"]["jurisdicciones"][j]["saldo_favor"]["periodo_mes"]
        monto_favor = self.data["payload"]["jurisdicciones"][j]["saldo_favor"]["monto"]
        if Decimal(monto_favor) > 0:
            select_anio.select_by_visible_text(str(anio))
            select_mes.select_by_visible_text(str(mes).title())
            monto = self.wait_and_go(xpath=XPATH_INPUT_MONTO_SALDO_FAVOR, click=False)
            monto.clear()
            monto.send_keys(str(monto_favor) + Keys.TAB + Keys.RETURN)

    def cargar_firmante(self):
        time.sleep(1)
        firmante = self.search_in_tree(class_tree="standartTreeRow", name="Datos del Firmante")
        firmante.click()
        self.go_right()
        apellido = self.wait_and_go(xpath=XPATH_APELLIDO_DDJJ, click=False)
        apellido.send_keys(str(self.data["payload"]["firmante"]["apellido"]))
        nombre = self.wait_and_go(xpath=XPATH_NOMBRE_DDJJ, click=False)
        nombre.send_keys(str(self.data["payload"]["firmante"]["nombre"]))
        mail = self.wait_and_go(xpath=XPATH_MAIL_DDJJ, click=False)
        mail.send_keys(str(self.data["payload"]["firmante"]["email"]))
        caracter = self.wait_and_go(xpath=SELECT_TITULAR, click=False)
        caracter = Select(caracter)
        caracter.select_by_visible_text("TITULAR")
        tipo_documento = self.wait_and_go(xpath=SELECT_TIPO_DOCUMENTO, click=False)
        tipo_documento = Select(tipo_documento)
        tipo_documento.select_by_visible_text(NAME_SELECT)
        numero_documento = self.wait_and_go(xpath=NUMERO_DOCUMENTO, click=False)
        numero_documento.send_keys(str(self.data["payload"]["firmante"]["cuit"]))
        self.wait_and_go(xpath="/html/body/div[1]/form/fieldset/div[7]/div[2]/input", click=True)

    def finalizar(self):
        self.go_left()
        time.sleep(1)
        finalizar = self.search_in_tree(class_tree=CLASS_TREE, name="Finalizar DDJJ")
        finalizar.click()
        self.go_right()
        time.sleep(2)
        self.wait_and_go(xpath=XPATH_XLS)
        name = "grid.xls"
        download_path = join(DOWNLOADS_PATH, self._id, name)
        while not exists(download_path):
            downloaded = False
        print("downloaded")
        time.sleep(5)
        with open(download_path, "rb") as d:
            xls = base64.b64encode(d.read())
            remove(download_path)
        self.wait_and_go(xpath=XPATH_CERRAR_DDJJ)
        time.sleep(1)
        alert = self.browser.switch_to.alert
        alert.accept()
        time.sleep(5)
        return xls

    def presentar(self, confirmar=False):
        filtro = self.wait_and_go(xpath=XPATH_FILTRO_PRESENTAR, click=False)
        anticipo = self.data["payload"]["presentar"]["anticipo"]
        filtro.send_keys(str(anticipo))
        if confirmar:
            time.sleep(2)
            acciones = self.browser.find_elements_by_xpath(XPATH_LISTA_CM03_ACTIONS)
            accion = "Presentar DDJJ ante AFIP"
            RESUMEN_FINDED = False
            for x in acciones:
                aux = x.get_attribute("title")
                if aux.upper() == accion.upper():
                    RESUMEN_FINDED = True
                    x.click()
                    time.sleep(2)
                    alert = self.browser.switch_to.alert
                    alert.accept()
                    # alert.dismiss()
                    time.sleep(60)
                    filtro = self.wait_and_go(xpath=XPATH_FILTRO_PRESENTAR, click=False)
                    filtro.clear()
                    filtro.send_keys(str(anticipo))
                    acciones = self.browser.find_elements_by_xpath(XPATH_LISTA_CM03_ACTIONS)
                    reporte = "Reporte de DDJJ"
                    REPORTE_FINDED = False
                    for y in acciones:
                        aux = y.get_attribute("title")
                        if aux.upper() == reporte.upper():
                            REPORTE_FINDED = True
                            y.click()
                            name = "DDJJ_Mensual_"
                            sfx = y.get_attribute("href").split("=")[-1]
                            name = name + str(sfx)
                            x.click()
                            time.sleep(2)
                            alert = self.browser.switch_to.alert
                            alert.dismiss()
                            time.sleep(10)
                            tmp = "/tmp/"
                            patron = re.compile(name.upper())
                            download = None
                            for z in listdir(join(tmp, str(self._id))):
                                if re.search(patron, z.upper()):
                                    with open(join(tmp, str(self._id), z), "rb") as f:
                                        download = base64.b64encode(f.read())
                                    remove(join(tmp, str(self._id), z))
                                    break
                            if not download:
                                log_prod.error("El resumen descargado no pude ser localizado")
                                raise FileNotFoundError("El resumen descargado no pude ser localizado")
                            return download
                    if not REPORTE_FINDED:
                        raise FileNotFoundError(f"No se pudo hallar el resumen para el anticipo {anticipo}")
                    break
            if not RESUMEN_FINDED:
                raise FileNotFoundError(f"No se pudo hallar la presentacion para el anticipo {anticipo}")
        else:
            return False

    def ddjj(self, t_s: float = None, t_o: float = None, headless: bool = None):
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.Sifereddjj.ddjj.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.Sifereddjj.ddjj.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.Sifereddjj.ddjj.headless", headless)
            self.run(t_s=t_s, headless=headless, t_o=t_o, c_d=True)
            self.select_cuit()
            self.wait_and_go(xpath=XPATH_SIFERE_DDJJ_NUEVA)
            select_anio = Select(self.wait_and_go(xpath=XPATH_SIFERE_DDJJ_ANIO, click=False))
            select_mes = Select(self.wait_and_go(xpath=XPATH_SIFERE_DDJJ_MES, click=False))
            select_anio.select_by_visible_text(str(self.data["payload"]["anio"]))
            select_mes.select_by_visible_text(str(self.data["payload"]["mes"]).title())
            self.wait_and_go(xpath=XPATH_SIFERE_DDJJ_CREAR)
            XPATH_ERROR = "/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr/td[1]/img"
            time.sleep(1)
            error = self.browser.find_elements_by_xpath(XPATH_ERROR)
            if len(error) > 0:
                indicador = error[0].get_attribute("src").split("/")[-1]
                if indicador.upper() == "ERROR.GIF":
                    text = self.wait_and_go(xpath="/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr/td[2]",
                                            click=False)
                    log_prod.error(f"{text.text}")
                    raise NotImplementedError(f"{text.text}")
            self.cargar_actividades()
            self.go_left()
            self.cargar_deducciones()
            self.go_left()
            self.cargar_actividades_juris()
            self.cargar_firmante()
            file = self.finalizar()
            presentar = bool(self.data["payload"]["presentar"]["presentar"])
            reporte = self.presentar(confirmar=presentar)
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                             payload={"xls descargado": str(file),
                                                      "DDJJ_Presentada.pdf": str(reporte)})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            self.logout()
            log_prod.info(f"job= {self._id}|END OF PROCESS")
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)


if __name__ == "__main__":
    from factory.servicios_varios import *
    inicio = SifereDDJJ(**ddjj_sifere)
    a = inicio.ddjj()
    print(a)