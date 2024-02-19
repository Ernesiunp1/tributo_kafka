import re
import time

from anfler_base.anfler_baseclass import BaseClass, log_prod
from anfler_agip.anfler_login import Login
from anfler_agip.settings import *
from anfler.util.msg import message as msg
from selenium.common.exceptions import WebDriverException
from anfler.util.helper import dpath
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from os.path import join, exists
from os import remove
import base64


class Esicol(BaseClass):

    def __init__(self, message: (dict, str), browser: str = "chrome",
                 t_s: float = 1, options: bool = True, *args, **kwargs):
        """
        :param message: json or dict with information 'cuit', 'password' in the key 'data'
        :param pwd: str contraseña de acceso del contribuyente
        :param pwd: tuple contiene 5 rutas de recorrido basico al destino en el siguiente orden
                    (XPATH_USERNAME, X_PATH_PASSWORD, XPATH_CCMA, XPATH_CALCULO_DEUDA, XPATH_BODY_DEUDA)
        """
        super(Esicol, self).__init__()  # por default la BaseClass corre chrome
        log_prod.info("INSTANCING ESICOL CLASS")
        self.data = self.validate_message(message)
        cuit, pwd = self.extract_cuit_pwd(self.data)
        self.cuit, self.pwd = self.validate(cuit, pwd)
        self._id = self.data["id"]
        self.browser = dpath(self.config, "scrapper.agip.esicol.browser", browser)
        self.t_s = dpath(self.config, "scrapper.agip.esicol.t_s", t_s)
        self.options = dpath(self.config, "scrapper.agip.esicol.options", options)

    def run(self, t_s: float = 1, t_o: float = None, headless: bool = None, c_d: bool = False):
        try:
            self.browser = Login(self.cuit,
                                 self.pwd,
                                 browser=self.browser,
                                 t_s=t_s,
                                 t_o=t_o,
                                 id_=self._id, change_dir=c_d).run(options=self.options,
                                                   headless=headless)
            XPATH_ESICOL = "//*[@id='aplicaciones']/div[9]/div[1]"
            self.wait_and_go(xpath=XPATH_ESICOL, click=False)
            name = "e-Sicol"
            self.force_find_xpath(self.browser, xpath=XPATH_APLICACIONES, group=True, name=name, click=True)
            return self
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def search_tree(self, xpath, name):
        time.sleep(10)
        trees = self.browser.find_elements_by_xpath(xpath)
        for x in trees:
            if x.text.upper() == name.upper():
                return x
        return False

    def saldo_favor(self, t_s: float = 1, headless: bool = None, t_o: float = None):
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.agip.esicol.saldo_favor.t_o", t_o)
            t_s = dpath(self.config, "scrapper.agip.esicol.saldo_favor.t_s", t_s)
            headless = dpath(self.config, "scrapper.agip.esicol.saldo_favor.headless", headless)
            self.run(headless=headless, t_s=t_s, t_o=t_o)
            self.wait_and_go(xpath=XPATH_DDJJ_PRESENTADA, click=True)
            ultima = self.wait_and_go(xpath=XAPTH_ULTIMA_PRESENTADA, click=False)
            accion = ActionChains(self.browser)
            accion.double_click(ultima).perform()
            self.browser.set_window_size(width=1980, height=1080)
            accion = ActionChains(self.browser)
            lyp = self.search_tree(xpath=XPATH_ESICOL_DDJJ_TREE, name="Liquidación del Impuesto y Presentación")
            accion.move_to_element_with_offset(to_element=lyp, xoffset=-20, yoffset=2).click().perform()
            saf = self.wait_and_go(xpath=XPATH_ESICOL_SALDO_RESULTANTE, click=False)
            assert saf.text.startswith("Subtotal a favor del Contribuyente"), \
                "NO se encontro el saldo en la declaración jurada"
            saf = saf.text.replace("Subtotal a favor del Contribuyente", "")
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                             payload={"Subtotal a favor del Contribuyente": saf})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            log_prod.info("END OF PROCESS: Sending response")
            self.logout()
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def descarga_ddjj(self, t_s: float = 1, headless: bool = None, t_o: float = None):
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.agip.esicol.descarga_ddjj.t_o", t_o)
            t_s = dpath(self.config, "scrapper.agip.esicol.descarga_ddjj.t_s", t_s)
            headless = dpath(self.config, "scrapper.agip.esicol.descarga_ddjj.headless", headless)
            self.run(headless=headless, t_o=t_o, t_s=t_s, c_d=True)
            self.wait_and_go(xpath=XPATH_DDJJ_PRESENTADA, click=True)
            time.sleep(5)
            ddjjs = self.browser.find_elements_by_class_name(CLASS_DDJJ_PRESENTADA_PERIODO)
            for x in ddjjs:
                if x.text == self.data["payload"]["periodo"]:
                    x.click()
                    page = self.browser.find_element_by_tag_name("html")
                    page.send_keys(Keys.TAB+Keys.TAB+Keys.TAB+Keys.TAB+Keys.RETURN)
                    name = "ddjjpresentacion.pdf"
                    finded = False
                    if self.wait_download(join(DOWNLOADS_PATH, self._id, name)):
                        finded = True
                        with open(join(DOWNLOADS_PATH, self._id, name), "rb") as d:
                            response = base64.b64encode(d.read())
                            remove(join(DOWNLOADS_PATH, self._id, name))
                        response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                                         payload={name: str(response)})
                        response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
                        self.logout()
                        log_prod.info("END OF PROCESS: Sending response")
                        return response
                    if not finded:
                        raise FileNotFoundError(f"{name} no fue localizado entre las descargas")
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def vep(self, t_s: float = 1, headless: bool = None, t_o: float = None):
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.agip.esicol.vep.t_o", t_o)
            t_s = dpath(self.config, "scrapper.agip.esicol.vep.t_s", t_s)
            headless = dpath(self.config, "scrapper.agip.esicol.vep.headless", headless)
            self.run(headless=headless, t_o=t_o, t_s=t_s)
            self.wait_and_go(xpath="//*[@id='tool-1091-toolEl']", click=True)
            self.wait_and_go(id_="button-1049").click()
            time.sleep(5)
            columna1 = self.browser.find_elements_by_class_name(CLASS_DDJJ_PRESENTADA_PERIODO)
            columna2 = self.browser.find_elements_by_class_name(CLASS_DDJJ_PRESENTADA_PERIODO)
            periodo = self.data["payload"]["periodo"].split("-")
            periodo_ano = periodo[0]
            periodo_mes = periodo[1] if periodo[1][0] != str(0) else periodo[1][1]
            try:
                for x in range(len(columna1)):
                    if (columna1[x].text == periodo_ano) and (columna2[x+1].text == periodo_mes):
                        columna1[x].click()
                        break
            except IndexError:
                raise IndexError(f"No se pudo encontrar la ddjj de periodo {periodo_ano}-{periodo_mes}")
            page = self.browser.find_element_by_tag_name("html")
            page.send_keys(Keys.TAB + Keys.RETURN)
            self.wait_and_go(xpath=XPATH_VEP_CALCULAR, click=True)
            self.wait_and_go(xpath=XPATH_VEP_VEP, click=True)
            pagar = self.data["payload"]["medio_pago"].lower()
            self.wait_and_go(xpath=XPATH_DIC_PAGOS[pagar], click=True)
            page = self.browser.find_element_by_tag_name("html")
            if pagar == "pagomiscuentas":
                page.send_keys(Keys.TAB+Keys.TAB+Keys.TAB+Keys.RETURN)
            elif pagar == "interbanking":
                page.send_keys(Keys.TAB+Keys.TAB+Keys.RETURN)
            elif pagar == "link":
                page.send_keys(Keys.TAB+Keys.RETURN)
            else:
                raise KeyError(f"El medio de pago {pagar} no esta disponible")
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                             payload={f"vep generado satisfactoriamente por red {pagar}"})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            self.logout()
            log_prod.info("END OF PROCESS: Sending response")
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def ddjj(self, t_s: float = 1, headless: bool = None, t_o: float = None):
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.agip.esicol.ddjj.t_o", t_o)
            t_s = dpath(self.config, "scrapper.agip.esicol.ddjj.t_s", t_s)
            headless = dpath(self.config, "scrapper.agip.esicol.ddjj.headless", headless)
            self.run(headless=headless, t_s=t_s, t_o=t_o)
            self.wait_and_go(xpath=XPATH_CERRAR_DEFAULT)
            self.wait_and_go(xpath=XPATH_PANEL_LATERAL_DDJJ)
            self.wait_and_go(xpath=XPATH_NUEVA_DDJJ)
            self.wait_and_go(xpath=XPATH_DDJJ_ANIO_FLECHA)
            self.wait_and_go(clase=CLASS_DDJJ_ANIOS, click=False)
            anios = self.browser.find_elements_by_class_name(CLASS_DDJJ_ANIOS)
            for anio in anios:
                if anio.text == str(self.data["payload"]["anio"]):
                    anio.click()
            self.wait_and_go(xpath=XPATH_DDJJ_MES_FLECHA)
            meses = self.browser.find_elements_by_class_name(CLASS_DDJJ_ANIOS)
            for mes in meses:
                if mes.text.upper() == self.data["payload"]["mes"].upper():
                    mes.click()
            page = self.browser.find_element_by_tag_name("html")
            page.send_keys(Keys.TAB+Keys.TAB+Keys.RETURN)
            XPATH_C = "//*[@id='tool-1156-toolEl']"
            self.wait_and_go(xpath=XPATH_C)
            self.wait_and_go(xpath=XPATH_PANEL_LATERAL_DDJJ)
            XPATH_DDJJ_ORIGINAL = "//*[@id='ext-gen1373']/td/div/span"
            ddjj_original = self.wait_and_go(xpath=XPATH_DDJJ_ORIGINAL, click=False)
            ActionChains(self.browser).double_click(ddjj_original).perform()
            XPATH_INFO_CAL_IMP = "/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[1]/div/div/div[1]/div[5]/div/table/tbody/tr[9]/td/div/span"
            XPATH_DDJJ_LIST_ACTIVIDADES = "//td[2]/table/tbody/tr/td[2]/div"
            XPATH_OPTS_IN_LIST = "//div[*]/div/div"
            actividades_declaradas = self.data["payload"]["actividades"]
            for actividad_declarada in actividades_declaradas:
                self.wait_and_go(xpath=XPATH_INFO_CAL_IMP)
                self.go_html(sleep=2)
                self.wait_and_go(xpath=XPATH_DDJJ_LIST_ACTIVIDADES)
                aux = actividades_declaradas[actividad_declarada]
                time.sleep(2)
                options = self.browser.find_elements_by_xpath(XPATH_OPTS_IN_LIST)
                FINDED = False
                for option in options.copy():
                    codigo = str(option.text.split(" ")[0]).upper()
                    if str(aux["codigo"]).upper() == codigo:
                        FINDED = True
                        option.click()
                        # page = self.go_html()
                        base = aux["base_imponible"]
                        print(base, "esta")
                        # ActionChains(self.browser).click(page).send_keys(str(base)).perform()
                        XPATH_BASE = "//table[3]/tbody/tr/td[2]/table/tbody/tr/td/input"
                        XPATH_ALI = "//table[4]/tbody/tr/td[2]/table/tbody/tr/td[2]/div"
                        base_ = self.wait_and_go(xpath=XPATH_BASE, click=False)
                        base_.clear()
                        base_.send_keys(str(base))
                        alicuota = aux["alicuota"]
                        XPATH_ALI_ = f"//li[contains(.,'{str(alicuota)}')]"
                        # self.wait_and_go(xpath=XPATH_ALI)
                        # self.wait_and_go(XPATH_ALI_)
                        time.sleep(2)
                        c = self.browser.find_elements_by_xpath(XPATH_ALI)
                        c[0].click()
                        time.sleep(2)
                        c = self.browser.find_elements_by_xpath(XPATH_ALI_)
                        c[0].click()
                        XPATH_OBSERVACION = "//textarea"
                        obser = self.wait_and_go(xpath=XPATH_OBSERVACION, click=False)
                        observacion = aux.get("observacion", "Nada que agregar")
                        obser.clear()
                        obser.send_keys(str(observacion))
                        self.go_html()
                        XPATH_CERRAR = "/html/body/div[*]/div[1]/div/div/div/div[5]/img"
                        self.wait_and_go(xpath=XPATH_CERRAR)
                if not FINDED:
                    print(f"La actividad {actividades_declaradas[actividad_declarada]} no se encuentra entre las opciones disponibles")
                    #raise KeyError(f"La actividad {actividad_declarada} no se encuentra entre las opciones disponibles")
            for saldo in self.data["payload"]["saldos_favor"]:
                self._saldo_favor(aux=saldo)
            self.agentes()
            return self.browser
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def agentes(self):
        XPATH_AGENTES = "/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[1]/div/div/div[1]/div[5]/div/table/tbody/tr[17]/td/div/span"
        XPATH_CARGAR = "//div/input"
        XPATH_GUARDAR = "//div[12]/em/button/span[2]"
        self.wait_and_go(xpath=XPATH_AGENTES)
        self.go_html(n_tabs=5)  # boton importar
        time.sleep(2)
        r = self.browser.find_elements_by_name("ruta")
        print(r)
        if len(r) > 0:
            print("aca", r[0].text)
            ruta = r"/home/victor/PycharmProjects/ANFLER-APP/anfler-webscrap/anfler_agip/files/RentasCiudadEsicolPercepciones-06-2021.txt"
            r[0].send_keys(ruta)
        self.go_html(sleep=5)
        XPATH_ALERT_MESSAGE = "/html/body/div[*]/div[2]/div[1]/div/div[1]/svg/text/tspan"
        # message = self.wait_and_go(xpath=XPATH_ALERT_MESSAGE, click=False)
        message = self.browser.find_elements_by_tag_name("svg")
        if len(message) > 0:
            print("mee", message[0].text)
        XPATH_ACEPTAR = "//span[contains(.,'Aceptar')]"
        #self.wait_and_go(xpath=XPATH_ACEPTAR)

    def _saldo_favor(self, aux=None):
        if self.data["payload"].get("saldos_favor", False) and aux:
            mes = aux["mes"]
            anio = aux["anio"]
            importe_ = aux["importe"]
            XPATH_SALDO_FAVOR = "/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[1]/div/div/div[1]/div[5]/div/table/tbody/tr[13]/td/div/span"
            XPATH_MES = "//table[2]/tbody/tr/td[2]/table/tbody/tr/td[2]/div"
            XPATH_MES_LIST = f"//li[contains(.,'{str(mes).title()}')]"
            XPATH_ANIO = "//td[2]/table/tbody/tr/td[2]/div"
            XPATH_ANIO_LIST = f"//li[contains(.,'{str(anio)}')]"
            XPATH_IMPORTE_NOM = "//table[3]/tbody/tr/td[2]/table/tbody/tr/td/input"
            XPATH_RESOLUCION = "//table[6]/tbody/tr/td[2]/table/tbody/tr/td[2]/div"
            XPATH_RESOLUCION_0 = "//li[contains(.,'2013-99999999999-AGIP')]"
            XPATH_CERRAR_SALDOS = "/html/body/div[12]/div[1]/div/div/div/div[5]/img"
            self.wait_and_go(xpath=XPATH_SALDO_FAVOR)
            self.go_html()
            self.wait_and_go(xpath=XPATH_ANIO)
            self.wait_and_go(xpath=XPATH_ANIO_LIST)
            self.wait_and_go(xpath=XPATH_MES)
            self.wait_and_go(xpath=XPATH_MES_LIST)
            importe = self.wait_and_go(xpath=XPATH_IMPORTE_NOM, click=False)
            importe.send_keys(str(importe_))
            self.wait_and_go(xpath=XPATH_RESOLUCION)
            time.sleep(2)
            self.wait_and_go(xpath=XPATH_RESOLUCION_0)
            self.go_html(sleep=2)
            self.wait_and_go(xpath=XPATH_CERRAR_SALDOS)

    def go_html(self, n_tabs=1, sleep=1, enter=True):
        time.sleep(sleep)
        page = self.browser.find_element_by_tag_name("html")
        ns = ''
        for x in range(n_tabs):
            ns += Keys.TAB
        if enter:
            ns += Keys.RETURN
        page.send_keys(ns)
        return page

    def deuda(self, t_s: float = 1, headless: bool = None, t_o: float = None):
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.agip.esicol.deuda.t_o", t_o)
            t_s = dpath(self.config, "scrapper.agip.esicol.deuda.t_s", t_s)
            headless = dpath(self.config, "scrapper.agip.esicol.deuda.headless", headless)
            self.run(headless=headless, t_s=t_s, t_o=t_o)
            self.wait_and_go(xpath=XPATH_CERRAR_DEFAULT)
            self.wait_and_go(xpath=XPATH_PERIODOS_IMPAGOS)
            time.sleep(10)
            texto = self.browser.find_elements_by_class_name(CLASS_ESICOL_INNER)
            patron = re.compile(r"\$[^\]]+")
            to_process = []
            for x in texto:
                aux = x.text
                if re.findall(patron, aux):
                    to_process.append(float(aux.replace("$", "").replace(".", "").replace(",", ".")))
            result = 0
            for p in to_process:
                result += p
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                             payload={f"Deuda total": result})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            self.logout()
            log_prod.info("END OF PROCESS: Sending response")
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)


if __name__ == "__main__":
    from factory.servicios_varios import deuda_agip, ddjj_agip
    esicol = Esicol(**ddjj_agip)
    B = esicol.ddjj(t_o=60, headless=False)
    print(B)
