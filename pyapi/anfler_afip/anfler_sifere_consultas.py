from anfler_base.anfler_baseclass import BaseClass, log_prod
from anfler_afip.anfler_login import Login
from anfler.util.helper import dpath
from selenium.common.exceptions import SessionNotCreatedException, NoSuchWindowException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from anfler.util.msg import message as msg
import time
from anfler_afip.settings import *


class SifereConsultas(BaseClass):

    def __init__(self, message, browser: str = "chrome", t_s: float = 0.5,
                 options: bool = True, *args, **kwargs):
        super(SifereConsultas, self).__init__()
        log_prod.info("INSTANCING SIFERECONSULTAS CLASS")
        self.data = self.validate_message(message)
        cuit, pwd = self.extract_cuit_pwd(self.data)
        self.cuit, self.pwd = self.validate(cuit, pwd)
        self._id = self.data["id"]
        self.browser = dpath(self.config, "scrapper.afip.sifere_consultas.browser", browser)
        self.t_s = dpath(self.config, "scrapper.afip.sifere_consultas.t_s", t_s)
        self.options = dpath(self.config, "scrapper.afip.sifere_consultas.options", options)
        self.headless = dpath(self.config, "scrapper.afip.sifere_consultas.headless", True)

    def run(self, t_s: float = 1, t_o: float = None, headless: bool = None):
        log_prod.info("START BROWSER TO SIFERE")
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
            wait_ = WebDriverWait(self.browser, 60)
            if self.browser.current_url == URL1 or self.browser.current_url == URL0:
                log_prod.debug("=======================URL 1=====================")
                time.sleep(5)
                #wait_.until(EC.element_to_be_clickable((By.ID, ID_GROUP_URL1)),
                #            message=f"No {inv_xpath.get(ID_GROUP_URL1, ID_GROUP_URL1)}")
                search = self.force_find_xpath(browser=self.browser, xpath=XPATH_CAJAS_AFIP, max_r=30,
                                               t_s=t_s, group=True, name=NAME_SIFERE)
                if isinstance(search, AssertionError):
                    raise search
            elif self.browser.current_url == URL2:
                log_prod.debug("=======================URL 2=====================")
                wait_.until(EC.element_to_be_clickable((By.XPATH, XPATH_GROUP_URL2)),
                            message=f"No {inv_xpath.get(XPATH_GROUP_URL2, XPATH_GROUP_URL2)}")
                search = self.force_find_xpath(self.browser, XPATH_LISTA_URL_2, t_s=t_s, click=True,
                                               group=True, name=NAME_SIFERE)
                if isinstance(search, AssertionError):
                    raise search

            elif self.browser.current_url == URL3:
                log_prod.debug(f"job= {self._id} |=======================URL 3=====================")
                print('Estamos en URL3')
                time.sleep(10)
                try:
                    search = self.force_find_xpath(self.browser,
                                                   xpath=XPATH_CAJAS_NUEVO_12_2022,
                                                   t_s=t_s,
                                                   click=False,
                                                   group=True,
                                                   name="Convenio Multilateral – SIFERE WEB - DDJJ" )
                    self.browser.execute_script("arguments[0].scrollIntoView(true);", search)
                    time.sleep(1)
                    search.click()
                except:
                    log_prod.error(f"job= {self._id} | MONOTRIBUTO EN EL BUSCADOR")
                    print('Monotributo en buscador')
                    input_element = self.force_find_xpath(browser=self.browser,
                                                          xpath="/html/body/div/div/main/div/section/div/div[2]/div/div[1]/div/div/div[1]/input",
                                                          t_s=5)
                    input_element.send_keys('Convenio Multilateral – SIFERE WEB - DDJJ')
                    time.sleep(1)
                    modal_element = self.force_find_xpath(browser=self.browser,
                                                          xpath="/html/body/div/div/main/div/section/div/div[2]/div/div[1]/div/div/ul/li/a",
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
            return self.browser
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e, close=False)

    def get_jurisdiccion(self, t_s: float = None, t_o: float = None, headless: bool = None):
        log_prod.info("LOOKING FOR ACTIVITY IN CERTIFICATE IMAGE")
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.SifereConsultas.get_jurisdiccion.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.SifereConsultas.get_jurisdiccion.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.SifereConsultas.get_jurisdiccion.headless", headless)
            self.run(t_s=t_s, headless=headless, t_o=t_o)
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            self.get_status_200(self.browser)
            ventana_actual = self.browser.current_window_handle

            self.actual_window_2(browser=self.browser,
                                 from_id=[ventana_actual],
                                 n_windows_end=2,
                                 t_s=t_s)
            b = "/html/body/div[3]/div/table/tbody/tr/td[3]"
            jurisdiccion = self.force_find_xpath(browser=self.browser,
                                                 xpath=XPATH_JURISD_SIFERE,
                                                 group=False,
                                                 click=False)
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                             payload={"jurisdiccion sede": jurisdiccion.text})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            log_prod.info("END OF PROCESS: Sending response")
            self.logout()
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)


if __name__ == "__main__":
    from factory.servicios_varios import *
    inicio = SifereConsultas(**sifere_jurisdiccion)
    inicio.get_jurisdiccion()
