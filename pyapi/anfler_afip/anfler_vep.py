import time

from anfler_base.anfler_baseclass import BaseClass, log_prod
from anfler_afip.settings import *
from anfler_afip.anfler_login import Login
from selenium.common.exceptions import *
from anfler.util.msg import message as msg
from anfler.util.helper import dpath
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Vep(BaseClass):

    def __init__(self, message: (dict, str), browser="chrome", t_s: float = 0.5,
                 options: bool = True, *args, **kwargs):
        super(Vep, self).__init__(browser=browser)
        log_prod.info("INSTANCING CONSTANCIA CLASS")
        self.data = self.validate_message(message)
        # cuit, pwd = int(self.data["data"]["cuit"]), self.data["data"]["password"]
        cuit, pwd = self.extract_cuit_pwd(self.data)
        self.cuit, self.pwd = self.validate(cuit, pwd)
        self._id = self.data["id"]
        self.browser = dpath(self.config, "scrapper.afip.vep.browser", browser)
        self.t_s = dpath(self.config, "scrapper.afip.vep.t_s", t_s)
        self.options = dpath(self.config, "scrapper.afip.vep.options", options)
        self.headless = dpath(self.config, "scrapper.afip.vep.headless", True)

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
            wait = WebDriverWait(self.browser, 20)
            if self.browser.current_url == URL1 or self.browser.current_url == URL0:
                log_prod.debug(f"job= {self._id}|=======================URL 1=====================")
                wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_CAJAS_AFIP)))
                prueba = self.browser.find_element_by_xpath(XPATH_CAJAS_AFIP)
                log_prod.debug(f"accediendo a {prueba.text}")
                self.force_find_xpath(browser=self.browser, xpath=XPATH_CAJAS_AFIP, max_r=30,
                                      t_s=t_s, group=True, name=NAME_MONOTRIBUTO, fullmatch=False)
            elif self.browser.current_url == URL2:
                log_prod.debug(f"job= {self._id}|=======================URL 2=====================")
                wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_LISTA_URL_2)))
                self.force_find_xpath(self.browser, XPATH_LISTA_URL_2, t_s=t_s, click=True,
                                      group=True, name="Monotributo")

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
            self.browser.set_window_size(1920, 1080)
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_PAGOS)))
            self.force_find_xpath(self.browser, XPATH_PAGOS, max_r=100, t_s=t_s)
            self.browser.set_window_size(1920, 1080)
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BTNS_MONOTRIBUTO)))
            return self
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def mensual(self, t_s: float = 1, t_o: float = None, headless: bool = None):
        log_prod.info(f"job= {self._id}|START BROWSER TO CERTIFICATE")
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.vep.mensual.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.vep.mensual.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.vep.mensual.headless", headless)
            self.run(t_s=t_s, t_o=t_o, headless=headless)
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            self.get_status_200(self.browser)
            wait = WebDriverWait(self.browser, 20)
            self.force_find_xpath(browser=self.browser, xpath=XPATH_BTNS_MONOTRIBUTO,
                                  group=True, name="PAGAR", click=True, fullmatch=True)
            time.sleep(4)
            monto = self.browser.find_elements_by_xpath("/html/body/form/main/section/div/div/div/div[1]/div/table/tbody/tr[*]/td[*]/strong")
            monto = monto[-1].text if len(monto) > 0 else str(None)
            alerta = self.browser.find_elements_by_xpath("//*[@id='divVEPPendiente']")
            alerta = alerta[0].text.replace("\n", " ") if len(alerta) > 0 else str(None)
            tabla = self.browser.find_elements_by_xpath("/html/body/form/main/section/div/div/div/div[1]/div/table")
            tabla = tabla[0].text if len(tabla) > 0 else str(None)
            wait.until(EC.element_to_be_clickable((By.ID, "iFramePagoOnline")))
            frame = self.browser.find_element_by_id("iFramePagoOnline")
            self.browser.switch_to.frame(frame)
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_CAJAS_TIPO_PAGO_OTROS)))
            cajas = self.browser.find_elements_by_xpath(XPATH_CAJAS_TIPO_PAGO_OTROS)
            metodo = self.data["payload"]["red_pago"]
            finded = False
            for x in cajas:
                if x.get_attribute("title") == metodo:
                    finded = True
                    log_prod.warning(f"Generando vep para {x.get_attribute('title')}")
                    x.click()
                    break
            if finded:
                wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_VEP_GENERAR)))
                self.force_find_xpath(browser=self.browser, xpath=XPATH_VEP_GENERAR, click=True)
                confirmacion = "/html/body/form/main/section/div/div/div/div[1]/div/div/div[3]/p"
                wait.until(EC.element_to_be_clickable((By.XPATH, confirmacion)))
                resumen = self.force_find_xpath(browser=self.browser, xpath=confirmacion, click=False)
                resumen = f"VEP confirmado para la obligacion {resumen.text}, por le metodo de pago: {metodo}"
                response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                                 payload={"resumen": resumen, "monto": monto,
                                                          "alerta": alerta, "tabla": tabla})
                response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
                self.logout()
                return response
            else:
                raise NoSuchElementException("No se pudo encontrar el metodo de pago indicado en la web")
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def total(self, t_s: float = 1, t_o: float = None, headless: bool = None):
        log_prod.info(f"job= {self._id}|START BROWSER TO CERTIFICATE")
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.vep.total.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.vep.total.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.vep.mensual.headless", headless)
            self.run(t_s=t_s, t_o=t_o, headless=headless)
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            self.get_status_200(self.browser)
            wait = WebDriverWait(self.browser, 20)
            self.force_find_xpath(browser=self.browser, xpath=XPATH_BTNS_MONOTRIBUTO,
                                  group=True, name="VER SALDO / PAGAR", click=True, fullmatch=True)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='btnConfirmar']")))
            self.force_find_xpath(browser=self.browser, xpath="//*[@id='btnConfirmar']", click=True)
            wait.until(EC.element_to_be_clickable((By.ID, "iFramePagoOnline")))
            frame = self.browser.find_element_by_id("iFramePagoOnline")
            self.browser.switch_to.frame(frame)
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_CAJAS_TIPO_PAGO_OTROS)))
            cajas = self.browser.find_elements_by_xpath(XPATH_CAJAS_TIPO_PAGO_OTROS)
            metodo = self.data["payload"]["red_pago"]
            finded = False
            for x in cajas:
                if x.get_attribute("title") == metodo:
                    finded = True
                    log_prod.warning(f"Generando vep para {x.get_attribute('title')}")
                    x.click()
                    break
            if finded:
                wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_VEP_GENERAR)))
                self.force_find_xpath(browser=self.browser, xpath=XPATH_VEP_GENERAR, click=True)
                confirmacion = "/html/body/form/main/section/div/div/div/div[1]/div/div/div[3]/p"
                wait.until(EC.element_to_be_clickable((By.XPATH, confirmacion)))
                resumen = self.force_find_xpath(browser=self.browser, xpath=confirmacion, click=False)
                resumen = f"VEP confirmado para la obligacion {resumen.text}, por le metodo de pago: {metodo}"
                response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]}, payload={"resumen": resumen})
                response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
                self.logout()
                return response
            else:
                raise NoSuchElementException("No se pudo encontrar el metodo de pago indicado en la web")
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)


if __name__ == "__main__":
    from factory.servicios_varios import vep_mensual
    vep = Vep(**vep_mensual)
    a = vep.mensual()
    print(a)
