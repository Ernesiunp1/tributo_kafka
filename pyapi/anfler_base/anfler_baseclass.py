from selenium.common import exceptions
from anfler_base.settings import *
import time
import anfler.util.log.lw as lw
import base64
import os
from io import StringIO
import requests
import re
import random
import anfler.util.config.cfg as cfg
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from anfler.util.helper import dpath
from os.path import join, exists
from selenium.webdriver.common.by import By
from anfler.util.msg import message as msg
import psutil
from glob import glob

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


log_dev = lw.get_logger("anfler.webscrap.dev")
log_prod = lw.get_logger("anfler.webscrap.prod")
if DEV:
    log_prod.info("Mode developer activated")
    print("estamos en desarrollo")
    # config_file_1 = "/home/ernesto/anfler/PYAPI-ULTIMO/pyapi/etc/config_afip.json"
    config_file_1 = "/home/victor/PycharmProjects/ANFLER-APP/anfler-webscrap/etc/config_afip.json"
    print("1", config_file_1)
    # config_file_2 = "/home/ernesto/anfler/PYAPI-ULTIMO/pyapi/etc/config_scrapper_ernesto.json"
    config_file_2 = "/home/victor/PycharmProjects/ANFLER-APP/anfler-webscrap/etc/config_scrapper_dev.json"
    print("2", config_file_2)
else:
    config_file_1 = "/app/etc/config_scrapper.json"
    config_file_2 = "/app/etc/config_afip.json"


class Wait(type):

    def __new__(meta, name, base, attr):
        t_meta = random.uniform(0, 2)
        time.sleep(t_meta)
        cfg.load([config_file_1, config_file_2], ignore_errors=False)
        # print("cfg.get dpath", dpath(cfg.get("scrapper"), "afip.time_out"))
        # print("cfgconfig", cfg.config)
        attr["cfg.config"] = cfg.config
        cls = type.__new__(meta, name, base, attr)
        return cls


class BaseClass(metaclass=Wait):
    """
    Clase anfler_base para automatizar tareas en plataformas web, por default inicia en URL_LOGIN_AFIP
    """

    def __init__(self, url: str = URL_LOGIN_AFIP, browser: str = "chrome",
                 t_s: float = 2, t_o: float = 10, id_: str = ""):
        self.url = url
        self.browser = browser
        self.config = cfg.config
        self.t_o = dpath(self.config, "scrapper.t_o", t_o)
        self.t_s = dpath(self.config, "scrapper.t_s", t_s)
        self._id = id_

    def logout(self, ):
        """Cierre del buscador, se recomienda sobreescribir con el cierre seguro de session de cada plataforma"""
        if isinstance(self.browser, (webdriver.Chrome, webdriver.Firefox)):
            self.browser.quit()
            time.sleep(2)
        else:
            pass

    def login(self, ):
        """Esta función debe implementar la logica de acceso a cada plataforma"""
        print("NO se ha implementado la clase login")
        return NotImplemented

    @staticmethod
    def extract_cuit_pwd(data):
        cuit_coded = data["header"]["auth"]["cuit"]
        pwd_coded = data["header"]["auth"]["password"]
        codif = data["header"]["auth"]["codif"]
        tipo = data["header"]["auth"]["type"]
        # TODO decodificar y retornar
        cuit_decoded = cuit_coded
        pwd_decoded = pwd_coded
        return cuit_decoded, pwd_decoded

    @staticmethod
    def validate(cuit: int, pwd: str) -> tuple:
        """
        Validation of type cuit and pwd
        :return: cuit, pwd if this have the correct type, else raise TypeError
        """
        log_prod.info("VALIDATING CUIT AND PWD")
        if cuit and pwd:
            if isinstance(cuit, int) and isinstance(pwd, str):
                return cuit, pwd
            else:
                msg = f"CUIT and pwd must be <class 'int'> and <class 'str'> but are {type(cuit)} and {type(pwd)}"
                log_prod.error(msg)
                raise Exception(TypeError, msg)

    @staticmethod
    def validate_message(message):
        log_prod.info("====================STARTING RUTINE====================")
        log_prod.info("VALIDATING MESSAGE")
        if isinstance(message, str):
            data = eval(message)
            error_msg = "message must be a of json, dict"
            if not isinstance(data, dict):
                log_prod.error(error_msg)
                raise TypeError(error_msg)
        elif isinstance(message, dict):
            data = message
        else:
            error_msg = "message format invalid, please send a dict or a json"
            log_prod.error(error_msg)
            raise TypeError(error_msg)
        return data

    def find_xpath(self, browser: webdriver, xpath: str, click: bool = True, t_s: float = None):
        """
        :browser: selenium webdriver where the XPATH will be searched
        :xpath: str its de xpath to find at de browser.
        :click: if True the object of the xpath will be clicked after be finded
        :t_s: float time sleep for wait between the xpath is finded and clicked or returned
        """
        log_prod.info(f"job= {self._id}|SEARCHING for xpath {inv_xpath.get(xpath, xpath)}")
        t_s = self.t_s if not t_s else t_s
        try:
            browser.set_window_size(1280, 720)
            # browser.set_page_load_timeout(t_o)
            time.sleep(t_s)
            obj = browser.find_element_by_xpath(xpath)
        except Exception as e:
            log_prod.error(str(e))
            return e
        time.sleep(t_s)
        if click:
            obj.click()
        return obj

    def find_xpaths(self, browser: webdriver, xpath: str,
                    click: bool = True, t_s: float = None, name: str = None, lista: bool = False, fullmatch=False):
        """
        :browser: selenium webdriver where the XPATH will be searched
        :xpath: str its de xpath to find at de browser.
        :click: if True the object of the xpath will be clicked after be finded
        :t_s: float time sleep for wait between the xpath is finded and clicked or returned
        """
        log_prod.warning(f"job= {self._id}|SEARCHING for xpaths {inv_xpath.get(xpath, xpath)}")
        t_s = self.t_s if not t_s else t_s
        try:
            browser.set_window_size(1280, 720)
            # browser.set_page_load_timeout(t_o)
            time.sleep(t_s)
            self.get_status_200(browser)
            obj = browser.find_elements_by_xpath(xpath)
            log_prod.info(">>>>>>>>>>>>>>>>FINDEDs<<<<<<<<<<<<<<<<<<<<")
            if lista:
                return obj
        except Exception as e:
            log_prod.error(str(e))
            return e
        time.sleep(t_s)
        d = {}
        for x in obj:
            d[x.text] = x
        if name:
            patron = re.compile(name.upper())
            # print("Patron: ", name)
            item = None
            for k, v in d.items():
                if re.search(patron, k.upper()) if not fullmatch else re.fullmatch(patron, k.upper()):
                    item = v
            if not item:
                log_prod.error(f"Not finded pattern: {name}")
                return AssertionError(f"Not finded pattern: {name}")
                # raise IndexError(f"Not finded pattern: {name}")
                # assert(item is not None)
            if click:
                item.click()
            return item
        if click:
            log_prod.debug("No se puede hacer click a una lista, diccionario")
        return d

    def force_find_xpath(self, browser, xpath, max_r: int = None, click: bool = True,
                         t_s: float = None, n=0, group: bool = False, name: str = None,
                         lista: bool = False, fullmatch: bool = False) -> object:
        """
        :browser: selenium webdriver where the XPATH will be searched.
        :xpath: str its de xpath to find at de browser.
        :max_r: int it's the number limit of recursion permited, the default max of python is 1000 we adopt this too.
        :click: if True the object of the xpath will be clicked after be finded.
        :t_s: float time sleep for wait between the xpath is finded and clicked or returned.
        :n: its a guide to count the number of recursion, don't change this or the number of recursion will be afected.
        """
        log_prod.warning(f"job= {self._id}|FORCING SEARCH OF XPATH: {inv_xpath.get(xpath, xpath)}")
        t_s = self.t_s if not t_s else t_s
        max_r = int(self.t_o/t_s) + 1
        log_prod.warning(f"N FOR CRASH: {max_r - n}")
        aux_browser = browser
        if group:
            obj = self.find_xpaths(browser, xpath, click, t_s, name=name, lista=lista)
        else:
            obj = self.find_xpath(browser, xpath, click, t_s)
        while isinstance(obj, exceptions.NoSuchElementException):
            n += 1
            if n >= max_r:
                error_msg = f"XPATH {xpath} not finded"
                log_prod.error(error_msg)
                raise Exception(exceptions.NoSuchElementException, error_msg)
            time.sleep(t_s)
            obj = self.force_find_xpath(browser=aux_browser, xpath=xpath,
                                        max_r=max_r, click=click, t_s=t_s,
                                        n=n, group=group)
            break
        log_prod.info("FINDED")
        return obj

    def find_id(self, browser: webdriver, ids: str, click: bool = True, t_s: float = None):
        """
        :browser: selenium webdriver where the XPATH will be searched
        :id: str its de xpath to find at de browser.
        :click: if True the object of the xpath will be clicked after be finded
        :t_s: float time sleep for wait between the xpath is finded and clicked or returned
        """
        log_prod.info(f"SEARCHING for id {ids}")
        try:
            t_s = self.t_s if not t_s else t_s
            obj = browser.find_element_by_id(ids)
        except Exception as e:
            log_prod.error(str(e))
            return e
        time.sleep(t_s)
        if click:
            obj.click()
        return obj

    def force_find_id(self, browser, ids, max_r: int = 100, click: bool = True, t_s: float = None, n=0) -> object:
        """
        :browser: selenium webdriver where the XPATH will be searched.
        :id: str its id to find at de browser.
        :max_r: int it's the number limit of recursion permited, the default max of python is 1000 we adopt this too.
        :click: if True the object of the xpath will be clicked after be finded.
        :t_s: float time sleep for wait between the xpath is finded and clicked or returned.
        :n: its a guide to count the number of recursion, don't change this or the number of recursion will be afected.
        """
        log_prod.warning(f"FORCING SEARCH OF id: {ids}")
        t_s = self.t_s if not t_s else t_s
        aux_browser = browser
        obj = self.find_xpath(browser, ids, click, t_s)
        while isinstance(obj, exceptions.NoSuchElementException):
            n += 1
            if n == max_r:
                error_msg = f"id {ids} not finded"
                log_prod.error(error_msg)
                raise Exception(exceptions.NoSuchElementException, error_msg)
            time.sleep(t_s)
            obj = self.force_find_xpath(browser=aux_browser, xpath=ids, max_r=max_r, click=click, t_s=t_s, n=n)
            break
        log_prod.info("FINDED")
        return obj

    def actual_window(self, browser, n_max, go_to, r_max=100, t_s: float = None):
        log_prod.info("SEARCHING for new tab")
        try:
            t_s = self.t_s if not t_s else t_s
            windows = browser.window_handles
            n = 0
            while len(windows) < n_max:
                n += 1
                windows = browser.window_handles
                if n >= r_max:
                    raise exceptions.NoSuchWindowException("No se pudo localizar la ventana de destino")
            try:
                browser.switch_to.window(windows[go_to])
            except Exception as e:
                log_prod.error(str(e))
                raise exceptions.NoSuchWindowException(f"Window no finded, {str(e)}")
            time.sleep(t_s)
            return browser
        except Exception:
            log_prod.error("No se creo la ventana esperada")
            self.logout()
            raise exceptions.NoSuchWindowException("No se creo la ventana esperada")

    def actual_window_2(self, browser, from_id, n_windows_end, t_s=1):
        log_prod.info("SEARCHING for new tab 2")
        try:
            wait = WebDriverWait(browser, 60)
            wait.until(EC.number_of_windows_to_be(n_windows_end))
            for window_handle in browser.window_handles:
                if window_handle not in from_id:
                    browser.switch_to.window(window_handle)
                    break
            return browser
        except Exception:
            log_prod.error("No se creo la ventana esperada")
            # self.logout()
            raise exceptions.NoSuchWindowException("No se creo la ventana esperada")

    def get_pdf_64(self, url, name):
        downloaded_obj = requests.get(url)
        encoded = base64.b64encode(downloaded_obj.content)
        # os.remove(DOWNLOADS_PATH+str(name))
        # shutil.rmtree(DOWNLOADS_PATH + str(self._id))
        return encoded

    @staticmethod
    def remove_tmp(name):
        patron = re.compile(name)
        l = [x for x in os.listdir(DOWNLOADS_PATH)]
        for x in l:
            if re.search(patron, x):
                log_prod.debug(f"finded and removing {x}")
                os.remove(DOWNLOADS_PATH + str(x))
            else:
                pass

    @staticmethod
    def opened_files(name):
        for proc in psutil.process_iter():
            try:
                flist = proc.open_files()
                if flist:
                    for nt in flist:
                        if nt.path == name:
                            return True
            except Exception as err:
                pass
        return False

    def wait_close(self, name):
        while self.opened_files(name):
            time.sleep(0.1)
        return True

    def get_csv_64(self, file_name, d_p=DOWNLOADS_PATH, max_time=360):
        log_prod.warning(f"job= {self._id} | DOCUMENTO a buscar para la descarga: {join( d_p, file_name)}")
        downloaded_file_name = join(d_p, file_name)
        log_prod.warning(f"job= {self._id} | FILE NAME CREATED : {downloaded_file_name} ")
        t = 0

        time.sleep(random.uniform(2, 5))
        
        if os.path.exists(downloaded_file_name):
            log_prod.warning(f"job={self._id} | FROM baseclass.py | get_csv_64 | DOWNLOADED_FILE_NAME EXISTE")
        else:
            log_prod.warning(f"job={self._id} | FROM baseclass.py | get_csv_64 | DOWNLOADED_FILE_NAME NO EXISTE")

            while not os.path.exists(downloaded_file_name):
                time.sleep(5)
                if t > max_time:
                    raise FileNotFoundError(
                        f"job_id={self._id} FROM baseclass.py| get_csv_64 |TimeOut while waiting file to be downloaded")
                t += 5

        log_prod.warning(f"job= {self._id} | DOCUMENTO ENCONTRADO EN LA DOWNLOAD_PATH, renaming")
        job_file_name = file_name.replace(".csv", f"_{self._id}.csv")
        job_file_path = join(d_p, job_file_name)
        time.sleep(3)
        os.renames(downloaded_file_name, job_file_path)
        with open(job_file_path, "r") as csv:
            stream = StringIO(csv.read())
            encoded = base64.b64encode(stream.getvalue().encode("utf-8"))
        csv.close()
        os.remove(job_file_path)
        return encoded

    def wait_and_go(self, xpath=None, id_=None, click=True, what="clickable", clase=None, mensaje=None):
        try:
            wait = WebDriverWait(self.browser, self.t_o)
            locator = None
            if xpath:
                mensaje = xpath if not mensaje else mensaje
                locator = (By.XPATH, xpath)
            if id_:
                mensaje = id_ if not mensaje else mensaje
                locator = (By.ID, id_)
            if clase:
                mensaje = clase if not mensaje else mensaje
                locator = (By.CLASS_NAME, clase)
            if what.upper() == "CLICKABLE":
                wait.until(EC.element_to_be_clickable(locator),
                           message=f"Esperando por: {inv_xpath.get(mensaje, mensaje)}")
            elif what.upper() == "VISIBLE":
                wait.until(EC.visibility_of_element_located(locator),
                           message=f"Esperando por: {inv_xpath.get(mensaje, mensaje)}")
            elif what.upper() == "WINDOW":
                actual = self.browser.current_window_handle
                n = int(len(self.browser.window_handles))+1
                wait.until(EC.number_of_windows_to_be(n), message=f"Esperando por: {inv_xpath.get(mensaje, mensaje)}")
                self.actual_window_2(self.browser, from_id=actual, n_windows_end=n)
                return self.browser
            else:
                raise KeyError("opcion de espera no implementada")
            if xpath:
                aux = self.force_find_xpath(self.browser, xpath, click=click)
                return aux
            elif id_:
                return self.browser.find_element_by_id(id_)
            elif clase:
                return self.browser.find_element_by_class_name(clase)
        except Exception:
            raise Exception(f"Error ocurrido durante la busqueda de xpath={inv_xpath.get(xpath, xpath)}, "
                            f"class={inv_xpath.get(clase, clase)}, id_={inv_xpath.get(id_, id_)}")

    @staticmethod
    def decode_csv_64(string):
        return base64.b64decode(eval(string)).decode("utf-8")

    @staticmethod
    def get_status_200(browser):
        a = requests.get(browser.current_url)
        if a.status_code == 200 or 403:
            return True
        else:
            error_msg = f"HTTP RESPONSE CODE STATUS NOT 200 AT {browser.current_url}"
            log_prod.error(error_msg)
            print(a.status_code)
            raise requests.exceptions.RequestException(error_msg)

    @staticmethod
    def get_status(browser):
        s = browser
        if isinstance(browser, (webdriver.Chrome, webdriver.Firefox)):
            urls_errors = {
                "https://servicios1.afip.gov.ar/tramites_con_clave_fiscal/ccam/app_offline.htm": "Página CCMA en Mtto",
                "https://monotributo.afip.gob.ar/app/Mantenimiento.aspx": "Página Monotributo en Mtto"
            }
            r = requests.get(browser.current_url)
            s = "HTTP CODE: " + str(r.status_code) + "| " + urls_errors.get(browser.current_url, "")
        elif browser == "chrome" or browser == "firefox":
            s = "El navegador fue cerrado subitamente"
        return s

    @staticmethod
    def validate_browser(browser):
        if isinstance(browser, (webdriver.Chrome, webdriver.Firefox)):
            return True
        else:
            return False

    @staticmethod
    def wait_download(name, t=60):
        if t < 1:
            t = 1
        READY = False
        n_ = 0
        while not READY or n_ > t:
            time.sleep(1)
            READY = exists(name)
            n_ += 1
        return READY

    def return_exception(self, browser, data, e, close=True):
        log_prod.error(f"job= {self._id}| {str(e)}")
        status_page = self.get_status(browser)
        if close:
            self.logout()
        response = msg.get_basic_message(header={"fn": data["header"]["fn"]}, payload={})
        response = msg.update_message(response, id=data["id"], errors=[status_page, str(e)], status=STATUS_FAIL)
        return response

    def return_simple_exception(self, browser, data, e, close=True):
        log_prod.error(f"job= {self._id} | FROM BASECLASS | RETURN_SIMPLE_EXCPTN | {browser}")
        log_prod.error(f"job= {self._id} | FROM BASECLASS | RETURN_SIMPLE_EXCPTN | {data}")
        time.sleep(random.uniform(1,3))
        if close:
            self.logout()

        response = msg.simple_message(e)

        return response
        
    def acceso_riesgos(self):
        self.browser.switch_to.frame("contenido")
        log_prod.warning(f"job={self._id} | ACCEDIENDO A IFRAME SIPER")

        xpath_tramites_boton = "/html/body/span/div[1]/aside/nav/ul/li[4]/a"
        xpath_siper_boton = '//*[@id="sectionContainer"]/article/div[4]/div[1]/div/div/div[2]/div[2]/div[2]/a'

        log_prod.warning(f"job={self._id} | FROM SIPER | BUSCANDO BOTON TRAMITES EN LISTA")
        self.force_find_xpath(browser=self.browser,
                              xpath=xpath_tramites_boton,
                              t_s=5,
                              click=True,
                              name='Trámites')
        log_prod.warning(f"job={self._id} | FROM SIPER | CLICK BOTON TRAMITES: OK")
        time.sleep(5)
        # wait_.until(EC.element_to_be_clickable((By.XPATH, xpath_siper_boton)))

        log_prod.warning(f"job={self._id} | FROM SIPER | BUSCANDO BOTON INGRESAR")
        self.force_find_xpath(browser=self.browser,
                              xpath=xpath_siper_boton,
                              t_s=5,
                              click=True,
                              name='INGRESAR')
        log_prod.warning(f"job={self._id} | FROM SIPER | CLICK BOTON TRAMITES: OK")
        time.sleep(5)

    def extraccion_datos_siper(self, riesgo=None):
        # EXTRAYENDO DATOS DE LA TABLA DE RIESGO

        try:
            # XPATHS PRINCIPALES DE TABLA DE RESULTADOS
            log_prod.warning(
                f'job: {self._id} | FROM SIPER | EXTRAYENDO DATOS DE RIESGO INTERNOS')
            letra = self.browser.find_element_by_xpath('//span[@class="calificacion"]').text
            texto = self.browser.find_element_by_xpath(
                '/html/body/div[2]/table[1]/tbody/tr[2]/td[3]/div/span[2]').text
            usuario = self.browser.find_element_by_xpath(
                '/html/body/div[2]/table[1]/tbody/tr[1]/td[3]/div').text
            try:
                motivo = self.browser.find_element_by_xpath(
                    '/html/body/div[2]/table[1]/tbody/tr[3]/td[3]/div').text

            except:
                motivo = "NO EXISTE MOTIVO"
                log_prod.warning(
                    f"job={self._id} | FROM SIPER | SIPER NO MUESTRA MOTIVO PARA USUARIO")

            try:
                fecha = self.browser.find_element_by_xpath(
                    '/html/body/div[2]/table[1]/tbody/tr[4]/td[3]/div').text
                riesgo["fecha"]: fecha
            except:
                fecha = "NO EXISTE FECHA"
                log_prod.warning(
                    f"job={self._id} | FROM SIPER | SIPER NO MUESTRA FECHA PARA USUARIO")

            try:
                extra_info = self.browser.find_element_by_xpath(
                    '/html/body/div[2]/table[2]/tbody/tr/td/div/ul/li').text
            except:
                extra_info = "NO EXISTE INFO EXTRA"
                log_prod.warning(f"job={self._id} | FROM SIPER | NO EXISTE INFORMACION EXTRA")

            riesgo = {"riesgo": letra,
                      "texto": texto,
                      "datos_Usuarios": usuario,
                      "motivo": motivo,
                      "fecha": fecha,
                      "extra_info": extra_info}

            return riesgo

        except Exception as e:
            log_prod.error(f"job={self._id} | FROM SIPER | ERROR: {e}")
            log_prod.error(f"job={self._id} | FROM SIPER | ERROR: {self.data}")
            log_prod.error(f"job={self._id} | FROM SIPER | ERROR: {self.browser}")
            return self.return_exception(self.browser, self.data, e)
 
    def status_clave(self, pwd):

        log_prod.warning(f"job={self._id} | FROM LOGIN | INICIALIZANDO VERIFICACION_STATUS_CLAVE")
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | BUSCANDO BTN CONTINUAR")
        btn_cambio_clave = self.browser.find_element_by_xpath("//input[@value='CONTINUAR']")
        btn_cambio_clave.click()
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | CLICK BTN CONTINUAR: OK")

        time.sleep(random.uniform(1, 3))
        input_clave = self.browser.find_element_by_xpath("//input[@placeholder='Tu clave']")
        input_clave.send_keys(pwd)
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | INGRESAR CALVE ACTUAL: OK")

        input_clave_nueva = self.browser.find_element_by_xpath("//input[@placeholder='Clave nueva']")
        input_clave_nueva.send_keys(f"{pwd}nueva")
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | INGRESAR CALVE NUEVA: OK")

        repite_clave_nueva = self.browser.find_element_by_xpath("//input[@placeholder='Repite tu clave nueva']")
        repite_clave_nueva.send_keys(f"{pwd}nueva")
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | CONFIRMAR CLAVE NUEVA: OK")

        btn_continuar = self.browser.find_element_by_xpath("//input[@value='CONTINUAR']")
        btn_continuar.click()
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | CLICK BTN CONTINUAR: OK")
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | NUEVA CLAVE ASIGNADA")

        time.sleep(random.uniform(2, 5))

        # BUSCANDO LOGIN PARA REVERTIR CLAVE
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | BUSCANDO LOGIN")
        wait_click = WebDriverWait(self.browser, 15)
        iconoChico = wait_click.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='iconoChicoContribuyenteAFIP']" )))
        btn_settings = iconoChico
        btn_settings.click()
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | CLICK LOGIN: OK")

        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | BUSCANDO CAMBIAR CLAVE EN MODAL")
        btn_settings_cambiar_clave = self.browser.find_element_by_xpath('//*[@id="contBtnContribuyente"]/div['
                                                                        '4]/button/div/div[2]')
        btn_settings_cambiar_clave.click()
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | CLICK CAMBIAR CLAVE EN MODAL: OK")

        time.sleep(random.randint(2, 3))

        ventanas = self.browser.window_handles

        self.browser.switch_to.window(ventanas[1])

        time.sleep(random.randint(1, 3))
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | CAMBIO DE VENTANA: OK")
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | BUSCANDO INPUT CLAVE")
        input_clave_actual = self.browser.find_element_by_xpath("//input[@placeholder='Tu clave']")
        input_clave_actual.send_keys(f"{pwd}nueva")
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | INPUT CLAVE: OK")

        time.sleep(random.randint(1, 3))

        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | BSCND INPUT REVERTIR CLAVE")
        input_nueva_clave = self.browser.find_element_by_xpath('//input[@placeholder="Tu nueva clave"]')
        input_nueva_clave.send_keys(pwd)
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | INPUT REVERTIR CLAVE: OK")

        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | BSCND INPUT CONFIRMAR EN REVERTIR CLAVE")
        input_confirma_clave = self.browser.find_element_by_xpath('//input[@placeholder="Repetí tu nueva clave"]')
        input_confirma_clave.send_keys(pwd)
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | INPUT CONFIRMAR EN REVERTIR CLAVE: OK")

        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | BSCND BTN CONTINUE")
        btn_cambio_clave = self.browser.find_element_by_xpath('//button[@id="continue-btn"]')
        btn_cambio_clave.click()
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | CLICK BTN CONTINUE: OK")

        time.sleep(random.uniform(1, 3))

        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | BSCND BOTON SI EN MODAL")
        btn_si_modal = self.browser.find_element_by_xpath('//button[@id="confirmar-cambio-clave-modal-si-btn"]')
        btn_si_modal.click()
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | CLICK BOTON SI EN MODAL: OK")
        try:
            confirmacion = self.browser.find_element_by_xpath('//span[@id="F1:msg-ok"]')
            if confirmacion:
                log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | REVERTIR CLAVE: OK!")
            else:
                log_prod.error(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | FUE IMPOSIBLE REVERTIR CLAVE")
        except:
            log_prod.error(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | FUE IMPOSIBLE REVERTIR CLAVE")

        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | CERRANDO VENTANA REVERTIR CLAVE")

        self.browser.close()

        self.browser.switch_to.window(ventanas[0])
        log_prod.warning(f"job={self._id} | FROM LOGIN | STATUS_CLAVE | MOVIENDO A VENTANA ACTUAL: OK")

        time.sleep(random.uniform(1, 2))

        actions = ActionChains(self.browser)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()

        return self.browser
    
    
    def __str__(self, ):
        text = f"BaseClass en url: {self.url}, usando el driver {self.browser}"
        return text
