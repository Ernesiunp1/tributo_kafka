from anfler_base.anfler_baseclass import BaseClass, log_prod
from anfler_afip.anfler_login import Login
from anfler.util.msg import message as msg
from anfler.util.helper import dpath
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException, NoSuchWindowException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from anfler_afip.settings import *
import time


class AltaMonotributo(BaseClass):

    def __init__(self, message: str, browser: str = "chrome", t_s: float = 2, options: bool = True, *args, **kwargs):
        super(AltaMonotributo, self).__init__()
        log_prod.info(f"job= {self._id}| ==================INSTANCING CLASS AltaMonotributo====================")
        self.data = self.validate_message(message)
        cuit, pwd = self.extract_cuit_pwd(self.data)
        self.cuit, self.pwd = self.validate(cuit, pwd)
        self.browser = dpath(self.config, "scrapper.afip.AltaMonotributo.browser", browser)
        self.t_s = dpath(self.config, "scrapper.afip.AltaMonotributo.t_s", t_s)
        self.options = dpath(self.config, "scrapper.afip.AltaMonotributo.options", options)
        self.headless = dpath(self.config, "scrapper.afip.AltaMonotributo.headless", True)
        self._id = self.data["id"]

    def step_1(self, t_s: float = 1, t_o: float = 30, headless: bool = None):
        try:
            log_prod.info(f"job= {self._id}| =================STEP_1================================")
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.ccma.run.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.ccma.run.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.ccma.run.headless", headless)
            self.browser = Login(cuit=self.cuit,
                                 pwd=self.pwd,
                                 browser=self.browser,
                                 t_s=t_s,
                                 t_o=t_o,
                                 id_=self._id).run(xpath=C_XPATHS_LOGIN,
                                                   options=self.options,
                                                   headless=False)
            return self.browser
        except (WebDriverException, Exception) as e:
            log_prod.error(f"job= {self._id}| {str(e)}")
            status_page = self.get_status(self.browser)
            self.logout()
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                             payload={})
            response = msg.update_message(response,
                                          id=self.data["id"],
                                          errors=[status_page, str(e)],
                                          status=STATUS_FAIL)
            return response

    def biometric(self):
        try:
            log_prod.info(f"job= {self._id}| =================Aceptacion de datos biometricos=======================")
            self.step_1()
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            wait_ = WebDriverWait(self.browser, 5)
            ventana_1 = self.browser.current_window_handle
            if self.browser.current_url == URL1:
                log_prod.debug("=======================URL 1=====================")
                search = self.force_find_xpath(browser=self.browser, xpath=XPATH_CAJAS_AFIP, max_r=30,
                                      group=True, name=NAME_ACEPTACION_BIOMETRICA)
                if isinstance(search, AssertionError):
                    raise search
                # En desuso por alternancia de AFIP
                # self.force_find_xpath(browser=self.browser, xpath=XPATH_MONOTRIBUTO, max_r=30, t_s=t_s)
            elif self.browser.current_url == URL2:
                log_prod.debug("=======================URL 2=====================")
                wait_.until(EC.element_to_be_clickable((By.XPATH, XPATH_GROUP_URL2)))
                search = self.force_find_xpath(self.browser, XPATH_LISTA_URL_2, click=True,
                                      group=True, name=NAME_ACEPTACION_BIOMETRICA)
                if isinstance(search, AssertionError):
                    raise search
            else:
                raise NoSuchWindowException("Se accedio a una ruta desconocida")
            self.actual_window_2(browser=self.browser, t_s=2, from_id=[ventana_1], n_windows_end=2)
            aceptado = self.force_find_xpath(browser=self.browser,
                                             xpath=XPATH_DATOS_ACEPTADOS,
                                             click=False,
                                             group=False)

            if aceptado.text == NAME_ACEPTADO:
                self.browser.close()
                self.browser.switch_to.window(ventana_1)
                return self.browser, ventana_1
            else:
                pass
        except (WebDriverException, Exception) as e:
            log_prod.error(f"job= {self._id}|{str(e)}")
            status_page = self.get_status(self.browser)
            self.logout()
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]}, payload={})
            response = msg.update_message(response, id=self.data["id"],
                                          errors=[status_page, str(e)], status=STATUS_FAIL)
            return response, 0

    def registral_system(self):
        try:
            self.browser, ventana_base = self.biometric()
            if self.browser.current_url == URL1 or self.browser.current_url == URL0:
                log_prod.debug("=======================URL 1=====================")
                self.force_find_xpath(browser=self.browser, xpath=XPATH_CAJAS_AFIP, max_r=30,
                                      group=True, name=NAME_SIS_REGISTRAL)
                # En desuso por alternancia de AFIP
                # self.force_find_xpath(browser=self.browser, xpath=XPATH_MONOTRIBUTO, max_r=30, t_s=t_s)
            elif self.browser.current_url == URL2:
                log_prod.debug("=======================URL 2=====================")
                self.force_find_xpath(self.browser, XPATH_LISTA_URL_2, click=True,
                                      group=True, name=NAME_SIS_REGISTRAL)
            else:
                raise NoSuchWindowException("Se accedio a una ruta desconocida")
            time.sleep(3)
            self.actual_window_2(browser=self.browser, from_id=[ventana_base], n_windows_end=2)
            self.browser.get("https://seti.afip.gob.ar/padron-puc-consulta-internet/rutOnBording")
            # rut = self.force_find_xpath(browser=self.browser, xpath=XPATH_RUT, click=False, group=True, name=NAME_RUT)
            # from selenium.webdriver import Chrome
            # driver = Chrome()
            # driver.fin
            # print(type(rut))
            # print(rut)
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)


if __name__ == "__main__":
    from factory.servicios_varios import *
    a = AltaMonotributo(**categoria)
    print(a.registral_system())
