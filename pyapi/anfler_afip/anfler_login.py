import os.path

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from anfler_base.anfler_baseclass import BaseClass, log_prod, log_dev
from anfler_base.decorators import random_wait
from anfler_afip.settings import *
from anfler.util.helper import dpath
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from os.path import join

from .cap_captcha import captchas_try


class Login(BaseClass):
    """Clase login para acceso a seccion monotributo AFIP"""

    def __init__(self, cuit: int, pwd: str, browser="chrome", t_s: float = 0.2, t_o: float = 60,
                 id_: str = None, change_dir=False):
        """
        :param cuit: int CUIT of taxpayer
        :param pwd: str contraseña of taxpayer
        """
        super(Login, self).__init__(browser=browser, id_=id_)  # por default la BaseClass corre chrome
        self.cuit, self.pwd = self.validate(cuit, pwd)
        # self.t_s = t_s
        # self.t_o = t_o
        self.t_s = dpath(self.config, "scrapper.t_s", t_s)
        self.t_o = dpath(self.config, "scrapper.t_o", t_o)
        self._change_dir = change_dir

    def change_dir(self, opciones: dict):
        new_dir = join("/tmp", self._id)
        opciones["download.default_directory"] = new_dir
        return opciones

    @random_wait()
    def run(self, xpath: tuple, t_s=None, t_o=None, options=True, headless=False) -> webdriver:
        """
        :xpath: tuple of two strings ('str', 'str') where index 0 its related to username and index 1 to password
        :t_s: float it's time sleep between all the steps of the workflow
        """
        log_prod.info(f"job= {self._id} |LOGGING AT URL: {self.url}")
        log_prod.info(f"job= {self._id} |SETTING OPTIONS OF DRIVER")
        t_o = self.t_o if not t_o else t_o
        t_s = self.t_s if not t_s else t_s
        try:
            # d_p = DOWNLOADS_PATH + self._id
            # if self._id not in os.listdir(DOWNLOADS_PATH):
            #     os.mkdir(d_p)
            if self.browser not in DRIVERS_ALLOWED.keys():
                error_msg = f"job= {self._id} |browser is not in settings.DRIVERS_ALLOWED"
                log_prod.error(error_msg)
                # assert (self.browser in DRIVERS_ALLOWED.keys()), log_prod.error(error_msg)
                raise NoSuchElementException(error_msg)
            if self.browser == "chrome":
                log_prod.info(f"job= {self._id} |====================DRIVER SELECTED: CHROME====================")
                if options:
                    opciones = webdriver.ChromeOptions()
                    opciones.arguments[:] = []
                    opciones.add_argument("--incognito")
                    opciones.add_argument("--crash-on-failure")
                    opciones.add_argument("--no-sandbox")
                    if headless:
                        opciones.add_argument("--headless")
                    opciones.add_argument('--disable-dev-shm-usage')
                    if self._change_dir:
                        OPTIONS_DRIVER["chrome"]["options"] = self.change_dir(OPTIONS_DRIVER["chrome"]["options"])
                    # opciones.add_argument("--remote-debugging-port=9515")
                    # o_d = OPTIONS_DRIVER["chrome"]["options"]
                    # o_d["download.default_directory"] = d_p  # DOWNLOADS_PATH + str(self._id)
                    # opciones.add_experimental_option("prefs", o_d)
                    opciones.add_experimental_option("prefs", OPTIONS_DRIVER["chrome"]["options"])
                    options = opciones
                self.browser = webdriver.Chrome(executable_path=OPTIONS_DRIVER["chrome"]["path"], options=options)
            elif self.browser == "firefox":
                log_prod.info(f"job= {self._id}| ====================DRIVER SELECTED: FIREFOX====================")
                if options:
                    from selenium.webdriver.firefox.options import Options
                    opciones = Options()
                    opciones.add_argument("--incognito")
                    if headless:
                        opciones.add_argument("--headless")
                    # opciones.set_preference("browser.download.dir", d_p)
                    opciones.set_preference("browser.download.dir", DOWNLOADS_PATH)
                    opciones.set_preference("browser.download.folderList", 2)
                    opciones.set_preference("browser.download.manager.showWhenStarting", False)
                    opciones.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
                    options = opciones
                if t_s < 2:
                    t_s = 2
                self.browser = webdriver.Firefox(executable_path=OPTIONS_DRIVER["firefox"]["path"], options=options,
                                                 firefox_options=options, log_path="logfirefox.log")
            self.browser.set_page_load_timeout(t_o)
            # self.browser.set_window_size(1280, 720)
            wait = WebDriverWait(self.browser, t_o)
            self.browser.get(self.url)
            # wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_DISTRACCION)))
            # self.wait_and_go(xpath=XPATH_DISTRACCION, mensaje=XPATH_DISTRACCION)
            # self.get_status_200(self.browser)
            # v_0 = self.browser.current_window_handle
            time.sleep(3)
            # self.actual_window_2(browser=self.browser, from_id=v_0, n_windows_end=2, t_s=2)
            # self.browser.close()
            # self.browser.switch_to.window(v_0)

            user = self.force_find_xpath(browser=self.browser, xpath=xpath[0], max_r=10, click=False, t_s=t_s)
            user.send_keys(f"{self.cuit}" + Keys.RETURN)
            time.sleep(t_s)
            errors = self.browser.find_elements_by_id('F1:msg')
            log_prod.warn(f"job= {self._id}|errores en user: {len(errors)}, {errors}")
            if len(errors) > 0:
                try:
                    cuit_invalido = bool(len(errors[0].text) > 0)
                except:
                    cuit_invalido = False
            elif len(errors) == 0:
                cuit_invalido = False
            else:
                log_prod.error("Existe una nueva rotacion en el DOM de AFIP login")
            if cuit_invalido:
                log_prod.error(f"job= {self._id}|INVALID USER")
                raise NoSuchElementException("CUIT invalid")
            else:
                
                captcha_response = captchas_try(self)
                if captcha_response == f'job= {self._id}|CAPTCHA INVALIDO':
                    raise NoSuchElementException('CAPTCHA INVALIDO')

                elif captcha_response == f"job= {self._id}|CLAVE INVALIDA FROM CAP_CAPTCHA":
                    raise NoSuchElementException('CLAVE INVALIDA FROM CAP_CAPTCHA')

                elif captcha_response == self.browser:
                    return self.browser
                

                wait.until(EC.element_to_be_clickable((By.XPATH, xpath[1])), message=f"Esperando {xpath[1]}")
                pwd = self.force_find_xpath(browser=self.browser, xpath=xpath[1], max_r=10, click=False, t_s=t_s)
                pwd.send_keys(f"{self.pwd}" + Keys.RETURN)
                time.sleep(t_s)
                errors = self.browser.find_elements_by_id('F1:msg')

                texto_error = ''
                
                try:
                    span_element = self.browser.find_element_by_id("F1:msg")
                    texto_error = span_element.text
                except Exception as e:
                    log_prod.warn(f"job= {self._id}|errores en pwd: {len(errors)}, {e}")                    
                

                log_prod.warn(f"job= {self._id}|errores en pwd: {len(errors)}, {texto_error}")
                if len(errors) > 0:
                    if texto_error =="Por medidas de seguridad tenés que cambiar tu contraseña":
                        log_prod.warning(f"job= {self._id}| DEBE CAMBIAR CLAVE FISCAL")
                        log_prod.warning(f"job= {self._id}| INICIALIZANDO CAMBIO DE CLAVE FISCAL")
                        # FUNCION QUE REALIZA EL CAMBIO DE CLAVE FISCAL (STATUS_CLAVE)
                        self.status_clave(self.pwd)
                        #raise NoSuchElementException("CAMBIAR CLAVE FISCAL")
                    elif texto_error =="Clave o usuario incorrecto":
                        log_prod.error(f"job= {self._id}|{texto_error}")
                        raise NoSuchElementException("Password invalid")
                    else:
                        log_prod.error(f"job= {self._id}|{texto_error}")
                        raise NoSuchElementException(f"MENSAJE DE ERROR DESDE EL LOGIN: {texto_error}")


            XPATH_TODOS = "/html/body/div/div/main/section[1]/div/div/div/div[5]/div/a"    # antiguo" ->  cambiado en 12-2022 /html/body/div/div/main/section[2]/div/div[3]/div[2]/div[4]/div[7]/div[1]/a"
            time.sleep(2)

                 ####  MANEJO DEL MODAL INCLUIDO POR AFIP 26/01/2023, APARECE JUSTO DESPUES DEL LOGIN #####
            #try:
                #MODAL = self.find_xpath('/html/body/div[2]/div[2]/div/div', 2)
                #if MODAL:


                    #log_prod.info('Se encontro el modal')
                    #BUTTON_CLOSE = '/html/body/div[2]/div[2]/div/div/div[3]/div/button[2]'
                    #self.wait_and_go(xpath=BUTTON_CLOSE, click=True)
                #else:
                    #print('No se encontro el modal')
                    #log_prod.info('NO SE ENCONTRO EL MODAL DESPUES DEL LOGING')
            #except:
                #print('No se encontro el modal')
                #log_prod.info('NO SE ENCONTRO EL MODAL DESPUES DEL LOGING')
        
                 ####  FIN DEL MANEJO DEL MODAL QUE APARECE DESPUES DEL LOGIN ####

            self.wait_and_go(xpath=XPATH_TODOS, click=True)
            # todos = self.browser.find_elements_by_xpath(XPATH_TODOS)
            # if len(todos) > 0: todos[0].click()
            log_prod.info(f"job= {self._id}|LOGGED continue")
            return self.browser
        except (WebDriverException, Exception) as e:
            log_prod.error(f"job= {self._id}|{str(e)}")
            status_page = self.get_status(self.browser)
            self.logout()
            return status_page + str(e)
