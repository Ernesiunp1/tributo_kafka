import re
from anfler_base.anfler_baseclass import BaseClass, log_prod, log_dev
from anfler_arba.anfler_login import Login
from anfler_arba.settings import *
from anfler.util.msg import message as msg
from selenium.common.exceptions import WebDriverException
from anfler.util.helper import dpath
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class CCMA(BaseClass):
    """Clase login para acceso a seccion monotributo AFIP"""

    def __init__(self, message: (dict, str), browser: str = "chrome",
                 t_s: float = 1, options: bool = True, *args, **kwargs):
        """
        :param message: json or dict with information 'cuit', 'password' in the key 'data'
        :param pwd: str contraseña de acceso del contribuyente
        :param pwd: tuple contiene 5 rutas de recorrido basico al destino en el siguiente orden
                    (XPATH_USERNAME, X_PATH_PASSWORD, XPATH_CCMA, XPATH_CALCULO_DEUDA, XPATH_BODY_DEUDA)
        """
        super(CCMA, self).__init__()  # por default la BaseClass corre chrome
        log_prod.info("INSTANCING CCMA CLASS")
        self.data = self.validate_message(message)
        # cuit, pwd = int(self.data["data"]["cuit"]), self.data["data"]["password"]
        cuit, pwd = self.extract_cuit_pwd(self.data)
        self.cuit, self.pwd = self.validate(cuit, pwd)
        self._id = self.data["id"]
        self.browser = dpath(self.config, "scrapper.arba.ccma.browser", browser)
        self.t_s = dpath(self.config, "scrapper.arba.ccma.t_s", t_s)
        self.options = dpath(self.config, "scrapper.arba.ccma.options", options)

    def resume(self, xpath: str = XPATH_CUENTA_CORRIENTE, t_s: float = 1, t_o: float = None,
               headless: bool = None, total=False):
        try:
            xpath = xpath if total else XPATH_DEUDA_IIBB
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.arba.ccma.resume.t_o", t_o)
            t_s = dpath(self.config, "scrapper.arba.ccma.resume.t_s", t_s)
            headless = dpath(self.config, "scrapper.arba.ccma.resume.headless", headless)
            self.browser = Login(self.cuit,
                                 self.pwd,
                                 browser=self.browser,
                                 t_s=t_s,
                                 t_o=t_o,
                                 id_=self._id).run(options=self.options,
                                                   headless=headless)
            resume = self.force_find_xpath(self.browser, xpath=xpath, click=False, max_r=30, t_s=t_s)
            resume = resume.text.replace('Pagá\n', '')
            name_payload = "resume" if total else "Deuda en IIBB"
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                             payload={f"{name_payload}": resume})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            self.logout()
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def positive_balance(self, xpath: str = XPATH_SALDO_FAVOR_TOTAL, t_s: float = 1,
                         t_o: float = None, headless: bool = None, total=False):
        try:
            xpath = xpath if total else XPATH_SALDO_FAVOR_IIBB
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.arba.ccma.positive_balance.t_o", t_o)
            t_s = dpath(self.config, "scrapper.arba.ccma.positive_balance.t_s", t_s)
            headless = dpath(self.config, "scrapper.arba.ccma.positive_balance.headless", headless)
            self.browser = Login(self.cuit,
                                 self.pwd,
                                 browser=self.browser,
                                 t_s=t_s,
                                 t_o=t_o,
                                 id_=self._id).run(options=self.options,
                                                   headless=headless)
            balance = self.force_find_xpath(self.browser, xpath=xpath, click=False, max_r=30, t_s=t_s)
            name_payload = "Balance positivo total" if total else "Balance positivo IIBB"
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                             payload={f"{name_payload}": balance.text})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            self.logout()
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def vep(self, t_s: float = 1, t_o: float = None, headless: bool = None):
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.arba.ccma.vep.t_o", t_o)
            t_s = dpath(self.config, "scrapper.arba.ccma.vep.t_s", t_s)
            headless = dpath(self.config, "scrapper.arba.ccma.vep.headless", headless)
            self.browser = Login(self.cuit,
                                 self.pwd,
                                 browser=self.browser,
                                 t_s=t_s,
                                 t_o=t_o,
                                 id_=self._id).run(options=self.options,
                                                   headless=headless)
            if not self.validate_browser(self.browser):
                raise KeyError("Cuit o Contraseña erronea")
            xp = "//*[@id='accordionInmo']/div/div[2]/app-ingresosbrutos/div"
            xp_text = "//*[@id='accordionInmo']/div/div[2]/app-ingresosbrutos/div/div[1]/a/div/div[1]/h3"
            wait = WebDriverWait(self.browser, t_o)
            wait.until(EC.element_to_be_clickable((By.XPATH, xp)), message=f"Esperando {xp}")
            t_ib = self.force_find_xpath(browser=self.browser, xpath=xp_text, click=False)
            t_ib = t_ib.text.split(" ")
            t_ib = " ".join(t_ib[1:])
            if t_ib.upper() == "INGRESOS BRUTOS":
                self.force_find_xpath(browser=self.browser, xpath=XPATH_PAGA_VEP_ARBA, click=True)
                actual = self.browser.current_window_handle
                self.actual_window_2(browser=self.browser, from_id=actual, n_windows_end=2)
                libre = self.browser.find_elements_by_xpath(XPATH_VEP_ARBA_LIBRE)
                if len(libre) > 0:
                    patron = re.compile(NAME_VEP_LIBRE)
                    for x in libre:
                        if re.search(patron, x.text):
                            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                                             payload={"Código de pago electronico": x.text})
                            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
                            self.logout()
                            return response
                self.force_find_xpath(browser=self.browser, xpath=XPATH_VEP_ARBA_ELECTRONICO, click=True)
                self.force_find_xpath(browser=self.browser, xpath=XPATH_VEP_ARBA_TODOS, click=True)
                self.force_find_xpath(browser=self.browser, xpath=XPATH_VEP_ARBA_CONTINUAR, click=True)
                wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_VEP_ARBA_MEDIOS)), message=f"Esperando {xp}")
                medios = self.browser.find_elements_by_xpath(XPATH_VEP_ARBA_MEDIOS)
                metodo = self.data["payload"]["red_pago"].upper()
                names_medios = [x.get_attribute("alt").upper() for x in medios]
                if metodo not in names_medios:
                    log_prod.error(f"Medio de pago {metodo} no fue encontrado, opciones disponibles: {names_medios}")
                    raise NameError(f"Medio de pago {metodo} no fue encontrado, opciones disponibles: {names_medios}")
                for x in medios:
                    if x.get_attribute("alt").upper() == metodo:
                        x.click()
                        wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_VEP_CODIGO)),
                                   message=f"Esperando {XPATH_VEP_CODIGO}")
                        codigo = self.force_find_xpath(browser=self.browser, xpath=XPATH_VEP_CODIGO, click=False)
                        response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                                         payload={"Código de pago electronico": codigo.text})
                        response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
                        self.logout()
                        return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)


if __name__ == "__main__":
    from factory.servicios_varios import *
    from pprint import pprint
    a = CCMA(**saldo_favor).positive_balance()
    # b = CCMA(**vep_iibb_arba).vep(headless=False)
    print(a)
    # print(b)
