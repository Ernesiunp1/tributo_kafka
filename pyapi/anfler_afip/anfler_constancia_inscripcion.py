import re

from anfler_base.anfler_baseclass import BaseClass, log_prod
from anfler_afip.settings import *
from anfler_afip.anfler_login import Login
from selenium.common.exceptions import *
from anfler.util.msg import message as msg
import time
from anfler.util.helper import dpath
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Constancia(BaseClass):

    def __init__(self, message: (dict, str), browser="chrome", t_s: float = 0.5,
                 options: bool = True, *args, **kwargs):
        super(Constancia, self).__init__(browser=browser)
        log_prod.info("INSTANCING CONSTANCIA CLASS")
        self.data = self.validate_message(message)
        cuit, pwd = self.extract_cuit_pwd(self.data)
        self.cuit, self.pwd = self.validate(cuit, pwd)
        self._id = self.data["id"]
        self.browser = dpath(self.config, "scrapper.afip.constancia_inscripcion.browser", browser)
        self.t_s = dpath(self.config, "scrapper.afip.constancia_inscripcion.t_s", t_s)
        self.options = dpath(self.config, "scrapper.afip.constancia_inscripcion.options", options)
        self.headless = dpath(self.config, "scrapper.afip.constancia_inscripcion.headless", True)

    def run(self, t_s: float = 1, t_o: float = None, headless: bool = None):
        log_prod.info(f"job= {self._id}|START BROWSER TO CERTIFICATE")
        try:
            self.browser = Login(self.cuit,
                                 self.pwd,
                                 browser=self.browser,
                                 t_o=t_o, id_=self._id).run(C_XPATHS_LOGIN,
                                              t_s=t_s,
                                              options=self.options,
                                              headless=headless)
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            # self.browser.maximize_window()
            wait = WebDriverWait(self.browser, 20)
            if self.browser.current_url == URL1 or self.browser.current_url == URL0:
                log_prod.debug(f"job= {self._id}|=======================URL 1=====================")
                # wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_CAJAS_AFIP)))
                # prueba = self.browser.find_element_by_xpath(XPATH_CAJAS_AFIP)
                time.sleep(15)
                prueba = self.wait_and_go(xpath=XPATH_CAJAS_AFIP, click=False)
                log_prod.debug(f"accediendo a {prueba.text}")
                search = self.force_find_xpath(browser=self.browser, xpath=XPATH_CAJAS_AFIP, max_r=30,
                                               t_s=t_s, group=True, name=NAME_MONOTRIBUTO, fullmatch=False)
                if isinstance(search, AssertionError):
                    raise search
            elif self.browser.current_url == URL2:
                log_prod.debug(f"job= {self._id}|=======================URL 2=====================")
                wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_LISTA_URL_2)),
                           message=f"Esperando {XPATH_LISTA_URL_2}")
                search = self.force_find_xpath(self.browser, XPATH_LISTA_URL_2, t_s=t_s, click=True,
                                      group=True, name="Monotributo")
                if isinstance(search, AssertionError):
                    raise search

            elif self.browser.current_url == URL3:
                log_prod.debug(f"job= {self._id} |=======================URL 3=====================")
                print('Estamos en URL3')
                time.sleep(10)
                log_prod.error(f"job= {self._id} | MONOTRIBUTO EN EL BUSCADOR")
                print('Monotributo en buscador')
                input_element = self.force_find_xpath(browser=self.browser,
                                                      xpath="/html/body/div/div/main/div/section/div/div[2]/div/div[1]/div/div/div[1]/input",
                                                      t_s=5)
                input_element.send_keys('Adhesión y/o empadronamiento al monotributo')
                time.sleep(1)
                modal_element = self.force_find_xpath(browser=self.browser,
                                                      xpath="/html/body/div/div/main/div/section/div/div[2]/div/div[1]/div/div/ul/li[1]/a",
                                                      t_s=5,
                                                      click=True,
                                                      name='Agregar')
                log_prod.info(f"job= {self._id} | SE AGREGO CAJA NUEVA MONOTRIBUTO Y SE ACCEDIO A ELLA ")
                time.sleep(1)
                time.sleep(t_s)

                if isinstance(input_element, AssertionError):
                    raise input_element


            else:
                raise NoSuchWindowException("Se accedio a una ruta desconocida")
            # self.browser = self.actual_window(browser=self.browser, n_max=2, go_to=1, t_s=t_s)
            window_actual_1 = self.browser.current_window_handle
            self.browser = self.actual_window_2(browser=self.browser, from_id=[window_actual_1], n_windows_end=2)
            self.browser.set_window_size(1920, 1080)
            XPATH_SELECT_USER_MONOTRIBUTO = "//div[@id='divRight']/div/div/a/div/div/div"
            XPATH_REPRESENTADO = "//*[@id='lnkRepresentando']/div"
            representado = self.browser.find_elements_by_xpath(XPATH_REPRESENTADO)
            if len(representado) > 0: representado[0].click()
            select_user = self.browser.find_elements_by_xpath(XPATH_SELECT_USER_MONOTRIBUTO)
            if len(select_user) > 0:
                select_user[0].click()
            XPATH_ALTA_MONOTRIBUTO = "//*[@id='bBtn1']"
            self.wait_and_go(xpath=XPATH_ALTA_MONOTRIBUTO, click=False)
            botones = self.browser.find_elements_by_xpath(XPATH_ALTA_MONOTRIBUTO)
            if len(botones) == 1:
                aux = botones[0].text.upper()
                patron = re.compile("DARSE DE ALTA")
                if re.search(patron, aux):
                    log_prod.error(f"{self._id}| Usuario no dado de alta como monotributista")
                    response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                                     payload={"Error": "Usuario no dado de alta como monotributista"})
                    response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
                    return response
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_CONSTANCIAS)),
                       message=f"Esperando {XPATH_CONSTANCIAS}")
            self.force_find_xpath(self.browser, XPATH_CONSTANCIAS, max_r=100, t_s=t_s)
            self.browser.set_window_size(1920, 1080)
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_VER_CONSTANCIA)))
            self.force_find_xpath(self.browser, XPATH_VER_CONSTANCIA, max_r=100, t_s=t_s)
            window_actual_2 = self.browser.current_window_handle
            self.browser = self.actual_window_2(browser=self.browser, from_id=[window_actual_1, window_actual_2],
                                                n_windows_end=3)
            # self.browser = self.actual_window(self.browser, 3, 2)
            # time.sleep(3)
            wait.until(EC.url_to_be("https://seti.afip.gob.ar/padron-puc-consulta-internet/AccessPointAction.do"))
            if self.get_status_200(self.browser):
                # select = self.force_find_xpath(browser=self.browser, xpath=XPATH_TIPO_CONSTANCIA, click=False, max_r=5)
                # wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_TIPO_CONSTANCIA)))
                self.browser.implicitly_wait(4)
                select = self.browser.find_elements_by_xpath(XPATH_TIPO_CONSTANCIA)
                if len(select) > 0:
                    if isinstance(select[0], webdriver.remote.webelement.WebElement):
                        select_object = Select(select[0])
                        select_object.select_by_visible_text(NAME_LISTA_OPTION)
                        wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_OPTION_CONTINUAR)))
                        self.force_find_xpath(browser=self.browser, xpath=XPATH_OPTION_CONTINUAR, click=True)
                        log_prod.info(f"job= {self._id}|DONE, WAITING FOR NEXT INSTRUCTION")
                        return self
                else:
                    log_prod.info(f"job= {self._id}|DONE, WAITING FOR NEXT INSTRUCTION")
                    return self
        except (WebDriverException, Exception) as e:
            raise NotImplementedError(str(e))

    def get_image(self, t_s: float = 1, t_f_i: float = 2, headless: bool = None, t_o: float = None) -> str:
        log_prod.info("LOOKING FOR CERTIFICATE IMAGE")
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.constancia_inscripcion.get_image.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.constancia_inscripcion.get_image.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.constancia_inscripcion.get_image.headless", headless)
            run = self.run(t_s=t_s, headless=headless, t_o=t_o)
            if isinstance(run, dict):
                raise AssertionError(str(run.get("errors", "Unknow error")))
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            self.get_status_200(self.browser)
            time.sleep(t_f_i)
            # self.browser.fullscreen_window()
            self.browser.set_window_size(1920, 1080)
            log_prod.debug(f"job= {self._id}| WAITING FOR: an entire image before take a screenshot ({t_f_i} seconds)")
            time.sleep(t_f_i)
            log_prod.debug(f"job= {self._id}|captura tomada de: {self.browser.current_url}")
            #if self.browser.current_url != "https://seti.afip.gob.ar/padron-puc-consulta-internet/AccessPointAction.do":
            #    raise NoSuchWindowException("No se llego a la url de la constancia esperada")
            imagen = self.browser.get_screenshot_as_base64()
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]}, payload={"image": imagen})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            self.logout()
            log_prod.info(f"job= {self._id}| END PROCESS: Sending response")
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def get_activity(self, t_s: float = None, headless: bool = None, t_o: float = None) -> str:
        log_prod.info(f"job= {self._id}| LOOKING FOR ACTIVITY IN CERTIFICATE IMAGE")
        try:
            t_o = self.t_o if not t_o else t_o
            # t_s = self.t_s if not t_s else t_s
            t_o = dpath(self.config, "scrapper.afip.constancia_inscripcion.get_activity.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.constancia_inscripcion.get_activity.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.constancia_inscripcion.get_activity.headless", headless)
            run = self.run(t_s=t_s, headless=headless, t_o=t_o)
            if isinstance(run, dict):
                raise AssertionError(str(run.get("errors", "Unknow error")))
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            wait = WebDriverWait(self.browser, 20)
            self.get_status_200(self.browser)
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_ACTIVIDAD_CONSTANCIA)))
            activity = self.force_find_xpath(browser=self.browser, xpath=XPATH_ACTIVIDAD_CONSTANCIA, group=True,
                                              name="ACTIVIDAD", click=False)
            # activity = self.force_find_xpath(self.browser, XPATH_ACTIVIDAD_CONSTANCIA, click=False, t_s=t_s)
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                             payload={"activity": activity.text})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            self.logout()
            log_prod.info(f"job= {self._id}| END PROCESS: Sending response")
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def get_address(self, t_s: float = 1.5, headless: bool = None, t_o: float = None) -> str:
        log_prod.info(f"job= {self._id}| LOOKING FOR ADDRESS IN CERTIFICATE IMAGE")
        try:
            t_o = self.t_o if not t_o else t_o
            # t_s = self.t_s if not t_s else t_s
            # headless = self.headless if not headless else headless
            t_o = dpath(self.config, "scrapper.afip.constancia_inscripcion.get_address.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.constancia_inscripcion.get_address.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.constancia_inscripcion.get_address.headless", headless)
            run = self.run(t_s=t_s, headless=headless, t_o=t_o)
            if isinstance(run, dict):
                raise AssertionError(str(run.get("errors", "Unknow error")))
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            self.get_status_200(self.browser)
            wait = WebDriverWait(self.browser, 20)
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_DIRECCION_CONSTANCIA1)))
            address_1 = self.force_find_xpath(self.browser, XPATH_DIRECCION_CONSTANCIA1, click=False)
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_DIRECCION_CONSTANCIA2)))
            address_2 = self.force_find_xpath(self.browser, XPATH_DIRECCION_CONSTANCIA2, click=False)
            address = address_1.text + ", " + address_2.text
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]}, payload={"address": address})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            self.logout()
            log_prod.info(f"job= {self._id}| END OF PROCESS: Sending response")
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def get_category(self, t_s: float = None, headless: bool = None, t_o: float = None):
        log_prod.info(f"job= {self._id}| LOOKING FOR CATEGORY IN CERTIFICATE IMAGE")
        try:
            t_o = self.t_o if not t_o else t_o
            # t_s = self.t_s if not t_s else t_s
            t_o = dpath(self.config, "scrapper.afip.constancia_inscripcion.get_category.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.constancia_inscripcion.get_category.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.constancia_inscripcion.get_category.headless", headless)
            run = self.run(t_s=t_s, headless=headless, t_o=t_o)
            if isinstance(run, dict):
                raise AssertionError(str(run.get("errors", "Unknow error")))
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            self.get_status_200(self.browser)
            wait = WebDriverWait(self.browser, 20)
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_CAT)), message=f"Esperando {XPATH_CAT}")
            cat = self.force_find_xpath(self.browser, XPATH_CAT)
            log_prod.info(f"job= {self._id}| END PROCESS: Sending response")
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]}, payload={"category": cat.text})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            self.logout()
            return response
        except (WebDriverException, Exception) as e:
            
            p_element = self.browser.find_element_by_css_selector("p")
            p_text = p_element.text
            if len(p_text) == 114:
                response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                                 payload={"category": p_text})
                self.browser.quit()
                return response
            

            return self.return_exception(self.browser, self.data, e)

    def get_startdate(self, t_s: float = None, headless: bool = None, t_o: float = None):
        log_prod.info(f"job= {self._id}| LOOKING FOR STARTDATE IN CERTIFICATE IMAGE")
        try:
            t_o = self.t_o if not t_o else t_o
            # t_s = self.t_s if not t_s else t_s
            t_o = dpath(self.config, "scrapper.afip.constancia_inscripcion.get_category.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.constancia_inscripcion.get_category.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.constancia_inscripcion.get_category.headless", headless)
            run = self.run(t_s=t_s, headless=headless, t_o=t_o)
            if isinstance(run, dict):
                raise AssertionError(str(run.get("errors", "Unknow error")))
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            self.get_status_200(self.browser)
            wait = WebDriverWait(self.browser, 20)
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_CAT)), message=f"Esperando {XPATH_CAT}")
            XPATH_STARTDATE = "/html/body/table[2]/tbody/tr[1]/td[2]/table/tbody/tr[13]/td/font"
            cat = self.wait_and_go(xpath=XPATH_STARTDATE, click=False)
            log_prod.info(f"job= {self._id}| END PROCESS: Sending response")
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]}, payload={"startdate": cat.text})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            self.logout()
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)


if __name__ == "__main__":
    from factory.servicios_varios import *

    ccma = {
        'message': {
            'status': 0,
            'errors': [],
            'id': '1234567890',
            'header': {
                'auth': {
                    'codif': 0,
                    'cuit': 20,
                    'password': "M1",
                    'type': 'basic'
                },
                'job_service': "afip",
                'fn': 'anfler_afip.anfler_validate_password.Validate@run',
                'offset': 0,
                'partition': 0
            },
            'payload': {},
        }
    }
    a = Constancia(**ccma)
    b = a.get_address()
    print(b)
