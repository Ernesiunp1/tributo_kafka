from anfler_base.anfler_baseclass import BaseClass, log_prod
from anfler_afip.anfler_login import Login
from anfler.util.msg import message as msg
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException, NoSuchWindowException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from anfler_afip.settings import *
import time


class Recategorizacion(BaseClass):

    def __init__(self, message: str, browser: str = "chrome", t_s: float = 2, options: bool = True, *args, **kwargs):
        super(Recategorizacion, self).__init__()
        log_prod.info(f"job= {self._id}| ==================INSTANCING CLASS RECATEGORIZACION====================")
        self.data = self.validate_message(message)
        cuit, pwd = self.extract_cuit_pwd(self.data)
        self.cuit, self.pwd = self.validate(cuit, pwd)
        self.browser = dpath(self.config, "scrapper.afip.recategorizacion.browser", browser)
        self.t_s = dpath(self.config, "scrapper.afip.recategorizacion.t_s", t_s)
        self.options = dpath(self.config, "scrapper.afip.recategorizacion.options", options)
        self.headless = dpath(self.config, "scrapper.afip.recategorizacion.headless", True)
        self._id = self.data["id"]

    def go(self, browser):
        try:
            self.force_find_xpath(browser=browser, xpath=XPATH_RECAT_CONT_1)
            categoria_nueva = self.force_find_xpath(browser=browser, xpath=XPATH_RECAT_CAT_NUEVA, click=False)
            categoria_nueva = categoria_nueva.text
            resumen_recat = self.force_find_xpath(browser=browser, xpath=XPATH_RECAT_RESUMEN, click=False)
            resumen_recat = resumen_recat.text
            # self.force_find_xpath(browser=self.browser, xpath=XPATH_RECAT_CONFIRMAR_CAT, click=True)
            confirmar = self.wait_and_go(id_="btnSiguiente", click=False)
            confirmar.click()
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]
                                                     },
                                             payload={"Categoria nueva": categoria_nueva,
                                                      "resumen": resumen_recat
                                                      })
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            self.logout()
            log_prod.info(f"job= {self._id}|END OF PROCESS")
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def run(self, t_s: float = 1, t_o: float = None, headless: bool = None):
        log_prod.info("START BROWSER TO CERTIFICATE")
        try:
            if not headless:
                if not dpath(self.config, "scrapper.afip.recategorizacion.run.headless", None):
                    headless = self.headless
                else:
                    headless = dpath(self.config, "scrapper.afip.recategorizacion.run.headless", None)
            self.browser = Login(self.cuit,
                                 self.pwd,
                                 browser=self.browser,
                                 t_o=t_o, id_=self._id).run(C_XPATHS_LOGIN,
                                              t_s=t_s,
                                              options=self.options,
                                              headless=headless)
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            wait = WebDriverWait(self.browser, t_o)
            # self.browser.maximize_window()
            time.sleep(5)
            if self.browser.current_url == URL1 or self.browser.current_url == URL0:
                log_prod.debug("=======================URL 1=====================")
                search = self.force_find_xpath(browser=self.browser, xpath=XPATH_CAJAS_AFIP, max_r=30,
                                               t_s=t_s, group=True, name=NAME_MONOTRIBUTO, fullmatch=False)
                if isinstance(search, AssertionError):
                    raise search
            elif self.browser.current_url == URL2:
                log_prod.debug("=======================URL 2=====================")
                search = self.force_find_xpath(self.browser, XPATH_LISTA_URL_2, t_s=t_s, click=True,
                                               group=True, name="Monotributo")
                if isinstance(search, AssertionError):
                    raise search

            elif self.browser.current_url == URL3:
                log_prod.debug(f"job= {self._id} |=======================URL 3=====================")
                print('Estamos en URL3')
                time.sleep(10)
                search = self.force_find_xpath(self.browser,
                                               xpath=XPATH_CAJAS_NUEVO_12_2022,
                                               t_s=t_s,
                                               click=False,
                                               group=True,
                                               name=NAME_MONOTRIBUTO)
                self.browser.execute_script("arguments[0].scrollIntoView(true);", search)
                time.sleep(1)
                search.click()

                if isinstance(search, AssertionError):
                    raise search

            else:
                raise NoSuchWindowException("Se accedio a una ruta desconocida")
            window_actual_1 = self.browser.current_window_handle
            self.browser = self.actual_window_2(browser=self.browser, from_id=[window_actual_1], n_windows_end=2)
            time.sleep(2)
            XPATH_SELECT_USER_MONOTRIBUTO = "//div[@id='divRight']/div/div/a/div/div/div"
            select_user = self.browser.find_elements_by_xpath(XPATH_SELECT_USER_MONOTRIBUTO)
            if len(select_user) > 0:
                select_user[0].click()
            self.force_find_xpath(browser=self.browser,
                                  xpath="//*[@id='bBtn1']",
                                  click=True,
                                  name=NAME_RECATEGORIZAR.upper(), group=True)
            texto = self.force_find_xpath(browser=self.browser, xpath=XPATH_FACTURAS_EMITIDAS_REC, click=False)
            if not "$" in str(texto.text):
                raise NotImplementedError("La recategorización no esta disponible para el usuario, favor revisar "
                                          "manualmente")
            monto_emitidas = texto.text
            monto_emitidas = monto_emitidas.split("$")[1]
            monto_emitidas = monto_emitidas.replace(".", "")
            monto_emitidas = float(monto_emitidas.replace(",", "."))
            monto_emitidas = int(monto_emitidas)
            monto_emitidas = dpath(self.data, "message.payload.monto_facturado", monto_emitidas)
            self.force_find_xpath(browser=self.browser, xpath=XPATH_CONT_RECAT, click=True)
            input_facturado = self.force_find_xpath(browser=self.browser, xpath=XPATH_RECAT_MONTO_INPUT, click=False)
            input_facturado.send_keys(monto_emitidas)
            if self.data["payload"]["local"].upper() == "SI":
                self.force_find_xpath(browser=self.browser, xpath=XPATH_RECAT_RADIO_SI_1, click=True)
                eec = self.force_find_xpath(browser=self.browser, xpath=XPATH_EEC, click=False)
                eec_ = str(int(self.data["payload"]["Energia electrica consumida"]))
                eec.send_keys(eec_)
                sa = self.force_find_xpath(browser=self.browser, xpath=XPATH_SUP_AFEC, click=False)
                sa_ = str(int(self.data["payload"]["Superficie afectada"]))
                sa.send_keys(sa_)
                if self.data["payload"]["alquilado"].upper() == "SI":
                    self.force_find_xpath(browser=self.browser, xpath=XPATH_ALQ_RADIO_SI, click=True)
                    alq = self.force_find_xpath(browser=self.browser, xpath=XPATH_ALQ_CORRES, click=False)
                    alq_ = str(int(self.data['payload']['Alquileres correspondientes']))
                    alq.send_keys(alq_)
                    select = self.force_find_xpath(browser=self.browser, xpath=XPATH_SELECT_INM, click=False)
                    n_inm = Select(select)
                    n_inm_ = self.data["payload"]["cuantos inmuebles alquila"]
                    n_inm_d = {"0": "0 (cero)", "1": "1 (uno)", "2": "2 (dos)"}
                    n_inm.select_by_visible_text(n_inm_d[str(n_inm_)])
                    cuits = self.force_find_xpath(browser=self.browser,
                                                  xpath=XPATH_CUIT_LOCADOR,
                                                  group=True,
                                                  click=False,
                                                  lista=True)
                    l_cuits = self.data["payload"]["locadores"]
                    for x in range(len(l_cuits)):
                        cuits[x].send_keys(str(l_cuits[x])+Keys.TAB+Keys.RETURN)
                    response = self.go(self.browser)
                elif self.data["payload"]["alquilado"].upper() == "NO":
                    response = self.go(self.browser)
            elif self.data["payload"]["local"].upper() == "NO":
                self.force_find_xpath(browser=self.browser, xpath=XPATH_RECAT_RADIO_NO_1, click=True)
                response = self.go(self.browser)
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)


"""
if __name__ == "__main__":
    from factory.servicios_varios import *
    import os
    from pprint import pprint
    c = recategorizacion["message"]["header"]["auth"]["cuit"]
    pprint(recategorizacion)
    a = Recategorizacion(**recategorizacion)
    r = a.run()
    pprint(r)
"""