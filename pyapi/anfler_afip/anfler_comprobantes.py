from anfler_base.anfler_baseclass import BaseClass, log_dev, log_prod
from anfler_afip.anfler_login import Login
from anfler_afip.settings import *
from selenium.common.exceptions import *
from anfler.util.msg import message as msg
from anfler.util.helper import dpath
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import shutil
from json import dumps


class Comprobantes(BaseClass):

    def __init__(self, message: (dict, str), browser: str = "chrome", t_s: float = 0.5, options: bool = True):
        """
        :params message: str, dict it's message from kafka
        :browser str: default 'chrome' it's have the option autodownload configured to use other you want to change the
        OPTION_DRIVER at the file anfler_afip.settings
        """
        super(Comprobantes, self).__init__()
        log_prod.info("INSTANCING COPROBANTES CLASS")

        self.data = self.validate_message(message)
        cuit, pwd = self.extract_cuit_pwd(self.data)
        self.cuit, self.pwd = self.validate(cuit, pwd)
        # self.data = self.validate_message(message)
        # cuit, pwd = int(self.data["data"]["cuit"]), self.data["data"]["password"]
        # self.cuit, self.pwd = self.validate(cuit, pwd)

        # self.browser = browser
        # self.options = options
        # self.t_s = t_s
        self._id = self.data["id"]
        self.browser = dpath(self.config, "scrapper.afip.comprobantes.browser", browser)
        self.options = dpath(self.config, "scrapper.afip.comprobantes.options", options)
        self.t_s = dpath(self.config, "scrapper.afip.comprobantes.t_s", t_s)
        self.headless = dpath(self.config, "scrapper.afip.comprobantes.headless", True)

    def run(self, t_s: float = None, headless: bool = None, t_o: float = None):
        try:
            log_prod.info("GOING TO 'COMPROBANTES'")
            # t_s = self.t_s if not t_s else t_s
            # t_o = self.t_o if not t_o else t_o
            self.browser = Login(browser=self.browser,
                                 cuit=self.cuit,
                                 pwd=self.pwd,
                                 id_=self._id).run(xpath=C_XPATHS_LOGIN, t_s=t_s,
                                                          options=self.options, headless=headless, t_o=t_o)
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            self.browser.set_page_load_timeout(t_o)
            self.browser.maximize_window()
            # self.force_find_xpath(self.browser, XPATH_COMPROBANTES, t_s=t_s)  # En desuso por alternancia de AFIP
            wait_ = WebDriverWait(self.browser, 60)
            if self.browser.current_url == URL1 or self.browser.current_url == URL0:
                log_prod.debug("=======================URL 1=====================")
                wait_.until(EC.element_to_be_clickable((By.ID, ID_GROUP_URL1)))
                self.force_find_xpath(self.browser, XPATH_CAJAS_AFIP, t_s=t_s,
                                      group=True, name=NAME_COMPROBANTES)
            elif self.browser.current_url == URL2:
                log_prod.debug("=======================URL 2=====================")
                wait_.until(EC.element_to_be_clickable((By.XPATH, XPATH_GROUP_URL2)))
                self.force_find_xpath(self.browser, XPATH_LISTA_URL_2, t_s=t_s, click=True,
                                      group=True, name=NAME_COMPROBANTES)


            elif self.browser.current_url == URL3:
                log_prod.debug(f"job= {self._id} |=======================URL 3=====================")
                print('Estamos en URL3')
                time.sleep(10)
                search = self.force_find_xpath(self.browser,
                                               xpath=XPATH_CAJAS_NUEVO_12_2022,
                                               t_s=t_s,
                                               click=False,
                                               group=True,
                                               name=NAME_COMPROBANTES )
                self.browser.execute_script("arguments[0].scrollIntoView(true);", search)
                time.sleep(1)
                search.click()

                if isinstance(search, AssertionError):
                    raise search


            else:
                raise NoSuchWindowException("Se accedio a una ruta desconocida")
            # self.browser = self.actual_window(self.browser, 2, 1, t_s=t_s)
            w_id = self.browser.current_window_handle
            self.actual_window_2(self.browser, from_id=[w_id], n_windows_end=2, t_s=t_s)
            wait_.until(EC.element_to_be_clickable((By.XPATH, XPATH_COMPROBANTES_REPRESENTAR)))
            self.force_find_xpath(self.browser, XPATH_COMPROBANTES_REPRESENTAR, t_s=t_s)
            wait_.until(EC.element_to_be_clickable((By.XPATH, XPATH_COMPROBANTES_CONSULTAS)))
            self.force_find_xpath(self.browser, XPATH_COMPROBANTES_CONSULTAS, t_s=t_s)
            desde, hasta = self.data["payload"]["from"], self.data["payload"]["to"]
            f = self.force_find_xpath(self.browser, XPATH_COMPROBANTES_CON_FROM, click=False)
            f.clear()
            f.send_keys(desde)
            t = self.force_find_xpath(self.browser, XPATH_COMPROBANTES_CON_TO, click=False)
            t.clear()
            t.send_keys(hasta)
            log_prod.info(f"job= {self._id} | DONE: WAITING FOR NEXT INTRUCTION")
            return self
        except (WebDriverException, Exception) as e:
            log_prod.error(f"job= {self._id} | Imposible loguearse por: {str(e)}")
            #self.logout()
            raise e

    def get_sales(self, t_s: float = 2, headless: bool = None, t_o: float = None):
        log_prod.info(f"job= {self._id} | GETTING SALES")
        try:
            # t_s = self.t_s if not t_s else t_s
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.comprobantes.get_sales.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.comprobantes.get_sales.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.comprobantes.get_sales.headless", headless)
            self.run(t_s=t_s, headless=headless, t_o=t_o)
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            wait_ = WebDriverWait(self.browser, 60)
            wait_.until(EC.element_to_be_clickable((By.XPATH, XPATH_BUSCAR_FACT_C)))
            self.get_status_200(self.browser)
            factura_c = self.force_find_xpath(self.browser, XPATH_FACTURA_C, click=False, t_s=t_s)
            error_msg = f"CRITICAL ERROR: Se detectó un cambio en la ubicación/nombre del documento 'Factura C' " \
                        f"por parte de AFIP, ahora se llama {factura_c.text}"
            assert (factura_c.text == "  Factura C"), log_dev.critical(error_msg)
            factura_c.click()
            self.force_find_xpath(self.browser, XPATH_PTO_VENTA, t_s=t_s)
            self.force_find_xpath(self.browser, XPATH_BUSCAR_FACT_C, t_s=t_s)
            # time.sleep(4)
            # lista = self.browser.find_elements_by_xpath(XPATH_FACTURA_C_VER)
            lista = self.force_find_xpath(browser=self.browser, xpath=XPATH_FACTURA_C_VER,
                                          click=False, group=True, lista=True)
            time.sleep(1)
            ventas = {}
            if len(lista) > 0:
                url_base = self.browser.current_url.split("/")
                url_base = [x+"/" for x in url_base[:-1]]
                url_base = "".join(url_base)
                for x in lista:
                    uri = x.get_attribute("onclick").split("=")
                    uri_ = uri[1] + "=" + uri[2]
                    url = (url_base + uri_).replace("'", "")
                    time.sleep(t_s)
                    self.browser.get(url)
                    # self.browser = self.actual_window(self.browser, 2, 1)
                    # w_id = self.browser.current_window_handle
                    # self.browser = self.actual_window_2(self.browser, from_id=w_id, n_windows_end=2, t_s=t_s)
                    # print(self.browser.current_url, url)
                    content = self.get_pdf_64(url, name=uri_)
                    self.remove_tmp(str(self.cuit))
                    ventas[f"{uri[2]}.pdf"] = str(content)
            log_prod.info("ENDING PROCESS AND SENDING RESPONSE")
            response = msg.get_basic_message()
            response = msg.update_message(response, header={"fn": self.data["header"]["fn"]},
                                          id=self.data["id"], status=STATUS_OK, payload={"ventas": ventas})
            # shutil.rmtree(DOWNLOADS_PATH + str(self._id))
            self.logout()
            return response
        except (WebDriverException, Exception) as e:
            status_page = self.get_status(self.browser)
            log_prod.error(f"job= {self._id} | {str(e)}")
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]})
            response = msg.update_message(response, id=self.data["id"],
                                          errors=[status_page, str(e)], status=STATUS_FAIL, payload={})
            self.logout()
            return response

    def get_purchases(self, t_s: float = 2, headless: bool = None, t_o: float = None):
        log_prod.info("GETTING PURCHASES")
        try:
            t_o = self.t_o if not t_o else t_o
            #t_s = self.t_s if not t_s else t_s
            t_o = dpath(self.config, "scrapper.afip.comprobantes.get_purchases.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.comprobantes.get_purchases.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.comprobantes.get_purchases.headless", headless)
            self.run(t_s=t_s, headless=headless, t_o=t_o)
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            self.get_status_200(self.browser)
            recibo_c = self.force_find_xpath(self.browser, XPATH_RECIBO_C, click=False, t_s=t_s)
            error_msg = f"CRITICAL ERROR: Se detectó un cambio en la ubicación/nombre del documento 'Recibo C' " \
                        f"por parte de AFIP, ahora se llama {recibo_c.text}"
            assert (recibo_c.text == "  Recibo C"), log_dev.error(error_msg)
            recibo_c.click()
            self.force_find_xpath(self.browser, XPATH_PTO_VENTA, t_s=t_s)
            self.force_find_xpath(self.browser, XPATH_BUSCAR_FACT_C, t_s=t_s)
            time.sleep(4)
            # lista = self.browser.find_elements_by_xpath(XPATH_FACTURA_C_VER)
            lista = self.force_find_xpath(browser=self.browser, xpath=XPATH_FACTURA_C_VER,
                                          click=False, group=True, lista=True)
            time.sleep(1)
            compras = {}
            if len(lista) > 0:
                url_base = self.browser.current_url.split("/")
                url_base = [x + "/" for x in url_base[:-1]]
                url_base = "".join(url_base)
                for x in lista:
                    uri = x.get_attribute("onclick").split("=")
                    uri_ = uri[1] + "=" + uri[2]
                    url = (url_base + uri_).replace("'", "")
                    time.sleep(t_s)
                    self.browser.get(url)
                    # self.browser = self.actual_window(self.browser, 2, 1)
                    content = self.get_pdf_64(url)
                    self.remove_tmp(str(self.cuit))
                    compras[f"{uri[2]}.pdf"] = content
            log_prod.info("ENDING PROCESS AND SENDING RESPONSE")
            response = msg.get_basic_message()
            response = msg.update_message(response, header={"fn": self.data["header"]["fn"]},
                                          id=self.data["id"], status=STATUS_OK, payload={"compras": compras})
            # shutil.rmtree(DOWNLOADS_PATH + str(self._id))
            self.logout()
            return response
        except (WebDriverException, Exception) as e:
            status_page = self.get_status(self.browser)
            log_prod.error(f"job= {self._id} | {str(e)}")
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]})
            response = msg.update_message(response, id=self.data["id"],
                                          errors=[status_page, str(e)], status=STATUS_FAIL, payload={})
            self.logout()
            return response


if __name__ == "__main__":
    from factory.servicios_varios import *
    a = Comprobantes(**ventas1).get_sales()
    print(a)