import re
import time

from anfler_base.anfler_baseclass import BaseClass, log_prod
from anfler_agip.anfler_login import Login
from anfler_agip.settings import *
from anfler.util.msg import message as msg
from selenium.common.exceptions import WebDriverException
from anfler.util.helper import dpath
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from os.path import join, exists
from os import remove, listdir
import base64


class Arciba(BaseClass):

    def __init__(self, message: (dict, str), browser: str = "chrome",
                 t_s: float = 1, options: bool = True, *args, **kwargs):
        """
        :param message: json or dict with information 'cuit', 'password' in the key 'data'
        :param pwd: str contraseña de acceso del contribuyente
        :param pwd: tuple contiene 5 rutas de recorrido basico al destino en el siguiente orden
                    (XPATH_USERNAME, X_PATH_PASSWORD, XPATH_CCMA, XPATH_CALCULO_DEUDA, XPATH_BODY_DEUDA)
        """
        super(Arciba, self).__init__()  # por default la BaseClass corre chrome
        log_prod.info("INSTANCING ARCIBA CLASS")
        self.data = self.validate_message(message)
        cuit, pwd = self.extract_cuit_pwd(self.data)
        self.cuit, self.pwd = self.validate(cuit, pwd)
        self._id = self.data["id"]
        self.browser = dpath(self.config, "scrapper.agip.arciba.browser", browser)
        self.t_s = dpath(self.config, "scrapper.agip.arciba.t_s", t_s)
        self.options = dpath(self.config, "scrapper.agip.arciba.options", options)

    def run(self, t_s: float = 1, t_o: float = None, headless: bool = None, c_d: bool = False):
        try:
            self.browser = Login(self.cuit,
                                 self.pwd,
                                 browser=self.browser,
                                 t_s=t_s,
                                 t_o=t_o,
                                 id_=self._id, change_dir=c_d).run(options=self.options,
                                                   headless=headless)
            self.wait_and_go(xpath=XPATH_ARCIBA, click=False)
            name = "Gestion-AR Agtes. de Recaudacion"
            self.force_find_xpath(self.browser, xpath=XPATH_APLICACIONES, group=True, name=name, click=True)
            return self
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def retenciones_percepciones(self, t_s: float = 1, headless: bool = None, t_o: float = None):
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.agip.arciba.retenciones_percepciones.t_o", t_o)
            t_s = dpath(self.config, "scrapper.agip.arciba.retenciones_percepciones.t_s", t_s)
            headless = dpath(self.config, "scrapper.agip.arciba.retenciones_percepciones.headless", headless)
            self.run(headless=headless, t_s=t_s, t_o=t_o, c_d=True)
            REGIMENES = ["retenciones", "percepciones", "retenciones bancarias", "percepciones aduaneras"]
            RESULTS = dict()
            for regimen in REGIMENES:
                log_prod.info(f"Buscando regimen {regimen}")
                self.wait_and_go(xpath=XPATH_ARCIBA_DESDE, click=True)
                self.wait_and_go(clase="datepicker-months")
                ano_desde = self.browser.find_elements_by_class_name("datepicker-switch")
                if len(ano_desde) == 3:
                    while int(ano_desde[1].text) != int(self.data["payload"]["ano_desde"]):
                        time.sleep(1)
                        accion = ActionChains(self.browser)
                        accion.move_to_element_with_offset(ano_desde[1], xoffset=-5, yoffset=5).click().perform()
                        ano_desde = self.browser.find_elements_by_class_name("datepicker-switch")
                meses_desde = self.browser.find_elements_by_class_name("month")
                succes = False
                for x in meses_desde:
                    if succes:
                        break
                    succes = False
                    if x.text.upper() == self.data['payload']['mes_desde'].upper():
                        x.click()
                        self.wait_and_go(clase="month", click=False)
                        ano_hasta = self.browser.find_elements_by_class_name("datepicker-switch")
                        if len(ano_hasta) == 3:
                            while int(ano_hasta[1].text) != int(self.data["payload"]["ano_hasta"]):
                                time.sleep(1)
                                accion = ActionChains(self.browser)
                                accion.move_to_element_with_offset(ano_hasta[1], xoffset=-5,
                                                                   yoffset=5).click().perform()
                                ano_hasta = self.browser.find_elements_by_class_name("datepicker-switch")
                        self.wait_and_go(clase="month", click=False)
                        meses_hasta = self.browser.find_elements_by_class_name("month")
                        for y in meses_hasta:
                            if y.text.upper() == self.data['payload']['mes_hasta'].upper():
                                y.click()
                                select_ = self.wait_and_go(xpath=XPATH_ARCIBA_SELECT_REGIMEN, click=False)
                                select_ = Select(select_)
                                select_.select_by_visible_text(regimen.title())
                                self.wait_and_go(xpath=XPATH_ARCIBA_BUSCAR, click=True)
                                time.sleep(5)
                                modal = self.browser.find_elements_by_class_name('modal-open')
                                print("aca modal", modal)
                                if len(modal) > 0:
                                    print("entre")
                                    XPATH_ARCIBA_CLOSE_MODAL = "//*[@id='myModalBtnClose']"
                                    self.wait_and_go(xpath=XPATH_ARCIBA_CLOSE_MODAL, click=True)
                                    RESULTS[regimen] = None
                                    succes = True
                                    break
                                else:
                                    self.wait_and_go(clase="dropdown-toggle", click=False)
                                    m = self.browser.find_elements_by_class_name("dropdown-toggle")
                                    for xx in m:
                                        if xx.text == "Ver Herramientas  ":
                                            xx.click()
                                    self.wait_and_go(clase="col-md-3", click=False)
                                    opt = self.browser.find_elements_by_class_name("col-md-3")
                                    patron = re.compile("Descargar Excel".upper())
                                    patron2 = re.compile("Descargar txt".upper())
                                    for xxx in opt:
                                        log_prod.warning("searching descargas ")
                                        if re.search(patron, xxx.text.upper()):
                                            log_prod.warning(f"Descarga Excel located")
                                            xxx.click()
                                            name_tabla = "RentasCiudad.csv"
                                            if self.wait_download(join(DOWNLOADS_PATH, self._id, name_tabla)):
                                                log_prod.warning(f"{name_tabla} descargado")
                                                with open(join(DOWNLOADS_PATH, self._id, name_tabla), "rb") as f:
                                                    response = base64.b64encode(f.read())
                                                    remove(join(DOWNLOADS_PATH, self._id, name_tabla))
                                                RESULTS[regimen] = {"csv": str(response)}
                                        elif re.search(patron2, xxx.text.upper()):
                                            log_prod.warning(f"Descarga txt located")
                                            xxx.click()
                                            time.sleep(20)
                                            downloads = listdir(join(DOWNLOADS_PATH, str(self._id)))
                                            name_txt = "RentasCiudadEsicol"
                                            patron3 = re.compile(name_txt.upper())
                                            for z in downloads:
                                                if re.search(patron3, z.upper()):
                                                    with open(join(DOWNLOADS_PATH, self._id, z), "rb") as txt:
                                                        aux = base64.b64encode(txt.read())
                                                        remove(join(DOWNLOADS_PATH, self._id, z))
                                                    RESULTS[regimen][z] = str(aux)
                                        else:
                                            log_prod.warning("yendo por else")
                                            continue
                                    XPATH_ARCIBA_CONSULTA = "/html/body/nav/div/div/div[2]/ul/li[1]/a"
                                    consulta = self.wait_and_go(xpath=XPATH_ARCIBA_CONSULTA, click=False)
                                    accion = ActionChains(self.browser)
                                    accion.move_to_element_with_offset(consulta, xoffset=2, yoffset=2).click().perform()
                                    succes = True
                                    break

            self.logout()
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                             payload={"Regimenes_and_Files": RESULTS})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            log_prod.info("END OF PROCESS: Sending response")
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)


if __name__ == "__main__":
    from factory.servicios_varios import retenciones_percepciones
    arciba = Arciba(**retenciones_percepciones)
    B = arciba.retenciones_percepciones(headless=True)
    print(B)