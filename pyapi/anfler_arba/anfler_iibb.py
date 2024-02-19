import base64
import os
import re
from anfler_base.anfler_baseclass import BaseClass, log_prod, log_dev
from anfler_arba.anfler_login import Login
from anfler_arba.settings import *
from anfler.util.msg import message as msg
from selenium.common.exceptions import WebDriverException
from anfler.util.helper import dpath
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from os.path import exists, join
from os import listdir
from selenium.webdriver.common.keys import Keys
import time


class IIBB(BaseClass):
    """Clase login para acceso a seccion monotributo AFIP"""

    def __init__(self, message: (dict, str), browser: str = "chrome",
                 t_s: float = 1, options: bool = True, *args, **kwargs):
        """
        :param message: json or dict with information 'cuit', 'password' in the key 'data'
        :param pwd: str contraseña de acceso del contribuyente
        :param pwd: tuple contiene 5 rutas de recorrido basico al destino en el siguiente orden
                    (XPATH_USERNAME, X_PATH_PASSWORD, XPATH_CCMA, XPATH_CALCULO_DEUDA, XPATH_BODY_DEUDA)
        """
        super(IIBB, self).__init__()  # por default la BaseClass corre chrome
        log_prod.info("INSTANCING CCMA CLASS")
        self.data = self.validate_message(message)
        cuit, pwd = self.extract_cuit_pwd(self.data)
        self.cuit, self.pwd = self.validate(cuit, pwd)
        self._id = self.data["id"]
        self.browser = dpath(self.config, "scrapper.arba.ccma.browser", browser)
        self.t_s = dpath(self.config, "scrapper.arba.ccma.t_s", t_s)
        self.options = dpath(self.config, "scrapper.arba.ccma.options", options)

    def run(self, t_s: float = 1, t_o: float = None, headless: bool = None, c_d: bool = False):
        try:
            self.browser = Login(self.cuit,
                                 self.pwd,
                                 browser=self.browser,
                                 t_s=t_s,
                                 t_o=t_o,
                                 id_=self._id, change_dir=c_d).run(options=self.options,
                                                   headless=headless)
            self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB, click=True)
            return self
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def iniciar(self, t_s: float = None, headless: bool = None, t_o: float = None) -> object:
        log_prod.info(f"job= {self._id}| WORKING ON INICIAR DDJJ IIBB")
        try:
            t_o = self.t_o if not t_o else t_o
            t_s = self.t_s if not t_s else t_s
            t_o = dpath(self.config, "scrapper.arba.iibb.presentacion.t_o", t_o)
            t_s = dpath(self.config, "scrapper.arba.iibb.presentacion.t_s", t_s)
            headless = dpath(self.config, "scrapper.arba.iibb.presentacion.headless", headless)
            self.run(t_s=t_s, headless=headless, t_o=t_o, c_d=True)
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            wait = WebDriverWait(self.browser, 20)

            self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_DDJJ, click=True)
            wait = WebDriverWait(self.browser, 20)
            wait.until(EC.number_of_windows_to_be(2))
            self.actual_window_2(browser=self.browser, from_id=[self.browser.current_window_handle], n_windows_end=2)
            self.browser.set_window_size(1920, 1080)
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_IIBB_PRES_DDJJ_2)))

            self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_DDJJ_2)
            self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_ANTICIPO)
            self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_ANTICIPO_INICIO)
            regimen = self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_SELECT_1, click=False)
            ano = self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_SELECT_2, click=False)
            mes = self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_SELECT_3, click=False)
            select1, select2, select3 = Select(regimen), Select(ano), Select(mes)
            regimen = self.data['payload'].get('regimen')
            ano = self.data['payload'].get('anio')
            if (regimen.upper() == "BIMESTRAL") and (int(ano) > 2008):
                raise TypeError("El regimen bimestral es valido solo en años anteriores al 2008")
            mes = self.data['payload'].get('mes')
            select1.select_by_visible_text(regimen)
            select2.select_by_visible_text(str(ano))
            select3.select_by_visible_text(str(mes))
            self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_ANTICIPO_BTN_INICIAR)
            return self
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def presentacion(self, ) -> object:
        log_prod.info(f"job= {self._id}| WORKING ON DETALLES DDJJ IIBB")
        try:
            self.iniciar()
            wait = WebDriverWait(self.browser, 20)
            html_ = self.browser.find_element_by_tag_name("html")
            h_w = html_.size
            h, w = h_w["height"], h_w["width"]
            factor_h, factor_w = 2.2, 1.57
            xoffset, yoffset = w/factor_w, h/factor_h
            action = ActionChains(self.browser)
            action.move_to_element_with_offset(to_element=html_, xoffset=xoffset, yoffset=yoffset).click().perform()
            self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_DETALLE_CARGA)
            alert = self.browser.switch_to.alert
            alert.accept()
            self.declaracion_actividades()
            name = "resumen"
            sfx1 = self.data["payload"]["anio"]
            sfx2 = self.data["payload"]["mes"]
            sfx2 = sfx2 if len(str(sfx2)) == 2 else "0" + str(sfx2)
            name = name + str(sfx1) + str(sfx2)
            self.find_xpath(self.browser, XPATH_IIBB_PRES_DDJJ_RESUMEN, click=True)
            time.sleep(5)
            tmp = "/tmp/"
            patron = re.compile(name.upper())
            download = None
            for x in listdir(join(tmp, str(self._id))):
                if re.search(patron, x.upper()):
                    with open(join(tmp, str(self._id), x), "rb") as f:
                        download = base64.b64encode(f.read())
                    os.remove(join(tmp, str(self._id), x))
            if not download:
                log_prod.error("El resumen descargado no pude ser localizado")
                raise FileNotFoundError("El resumen descargado no pude ser localizado")
            self.force_find_xpath(self.browser, XPATH_IIBB_PRES_DDJJ_ENVIAR, click=True)
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                             payload={"pdf resumen presentado": str(download)})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            self.logout()
            log_prod.info(f"job= {self._id}|END OF PROCESS")
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def declaracion_actividades(self):
        log_prod.info(f"job= {self._id}| WORKING ON DECLARION ACTIVIDADES DDJJ IIBB")
        try:
            wait = WebDriverWait(self.browser, 20)
            # wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_IIBB_PRES_DETALLE_CARGA_EDIT)))
            # self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_DETALLE_CARGA_EDIT)
            self.wait_and_go(xpath=XPATH_IIBB_PRES_DETALLE_CARGA_EDIT)
            monto_imponible = self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_DETALLE_EDIT_M_IMPON,
                                                    click=False)
            monto_imponible.send_keys(str(self.data["payload"]["monto_imponible"]))
            if self.data["payload"]["editar_alicuota"]:
                self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_EDIT_CHK)
                s_a = self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_EDIT_SELECT, click=False)
                select_ali = Select(s_a)
                p_new = self.data["payload"]["nueva_alicuota"]
                select_ali.select_by_visible_text(str(p_new))
            self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_EDIT_M_IMPON_BUT)
            alert = self.browser.switch_to.alert
            alert.accept()
            self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_EDIT_BUTT_BACK)
            self.deducciones()
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def deducciones(self):
        log_prod.info(f"job= {self._id}| WORKING ON DEDUCCIONES DDJJ IIBB")
        try:
            self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_EDIT_BUTT_DEDUCC)
            self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_DEDUCC_CARGA)
            self.browser.implicitly_wait(10)
            pestana = ["//a[contains(text(),'Retenciones')]",
                       "//a[contains(text(),'Percepciones')]",
                       "//a[contains(text(),'Percepciones aduaneras')]",
                       "//a[contains(text(),'Retenciones bancarias')]"]
            checks = ["//*[@id='selRetenciones']",
                      "//*[@id='selPercepciones']",
                      "//*[@id='selPercepcionesAduaneras']",
                      "//*[@id='selRetencionesBancarias']"]
            for x in range(4):
                self.wait_and_go(xpath=pestana[x], click=True)
                empty = self.browser.find_elements_by_xpath(f"//*[@id='tablaGrafico{x+1}']/tbody/tr/td")
                if empty[0].text.upper == "No hay información disponible.".upper():
                    continue
                else:
                    self.wait_and_go(xpath=checks[x], click=True)
            self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_DEDUCC_VOLVER)
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def descargar_retenc_percep(self, t_s: float = None, headless: bool = None, t_o: float = None):
        try:
            t_o = self.t_o if not t_o else t_o
            t_s = self.t_s if not t_s else t_s
            t_o = dpath(self.config, "scrapper.arba.iibb.descargar_retenc_percep.t_o", t_o)
            t_s = dpath(self.config, "scrapper.arba.iibb.descargar_retenc_percep.t_s", t_s)
            headless = dpath(self.config, "scrapper.arba.iibb.descargar_retenc_percep.headless", headless)
            self.run(headless=headless, t_o=t_o, t_s=t_s)
            # wait = WebDriverWait(self.browser, self.t_o)
            actual = self.browser.current_window_handle
            # wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_IIBB_DEDUCCIONES)),
            #            message=f"Esperando: {XPATH_IIBB_DEDUCCIONES}")
            # self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_DEDUCCIONES, click=True)
            self.wait_and_go(xpath=XPATH_IIBB_DEDUCCIONES)
            self.actual_window_2(self.browser, from_id=actual, n_windows_end=2)
            # wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_DEDUC_ROL_SELECC)))
            rol_select = self.wait_and_go(xpath=XPATH_DEDUC_ROL_SELECC, click=False)
            # rol_select = self.force_find_xpath(self.browser, XPATH_DEDUC_ROL_SELECT, click=False)
            rol_select = Select(rol_select)
            rol = self.data["payload"]["rol"]
            roles = [x.text for x in rol_select.options]
            if (len(roles) > 0) and rol not in roles:
                log_prod.error(f"El rol {rol} no coincide, roles disponibles: {str(rol_select.options)}")
                raise KeyError(f"El rol {rol} no coincide, roles disponibles: {str(rol_select.options)}")
            rol_select.select_by_visible_text(rol)
            # self.force_find_xpath(self.browser, XPATH_DEDUC_ROL_SELECC, click=True)
            self.wait_and_go(xpath=XPATH_DEDUC_ROL_SELECC)
            # wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_DEDUC_DEDUC)))
            # self.force_find_xpath(self.browser, XPATH_DEDUC_DEDUC)
            self.wait_and_go(xpath=XPATH_DEDUC_DEDUC)
            # self.force_find_xpath(self.browser, XPATH_DEDUC_DEDUC_DESC)
            self.wait_and_go(xpath=XPATH_DEDUC_DEDUC_DESC)
            # anio = self.force_find_xpath(self.browser, XPATH_DEDUC_DESC_ANIO, click=False)
            anio = self.wait_and_go(xpath=XPATH_DEDUC_DESC_ANIO, click=False)
            # mes = self.force_find_xpath(self.browser, XPATH_DEDUC_DESC_MES, click=False)
            mes = self.wait_and_go(xpath=XPATH_DEDUC_DESC_MES, click=False)
            anio.send_keys(self.data["payload"]["anio"])
            mes.send_keys(self.data["payload"]["mes"])
            # self.force_find_xpath(self.browser, XPATH_DEDUC_CONSULTAR)
            self.wait_and_go(xpath=XPATH_DEDUC_CONSULTAR)
            mensaje = self.find_xpaths(self.browser, XPATH_DEDUC_NO, lista=True)
            if len(mensaje) > 0:
                message = "No Existen archivos para a o periodo solicitado."
                if mensaje[0].text.upper() == message.upper():
                    log_prod.info("El contribuyente no presenta deducciones para el periodo considerado")
                    response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                                     payload={"Mensaje": message})
                    response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
                    self.browser.quit()
                    log_prod.info(f"job= {self._id}|END OF PROCESS")
                    return response
            # wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_DEDUC_DESCARGAR)))
            # self.force_find_xpath(self.browser, XPATH_DEDUC_DESCARGAR)
            self.wait_and_go(xpath=XPATH_DEDUC_DESCARGAR)
            file_name = str(f"-{self.cuit}-")
            patron = re.compile(file_name)
            time.sleep(10)
            for x in listdir(DOWNLOADS_PATH):
                if re.search(patron, x) and x.endswith(".zip"):
                    file_name = x
                    break
            with open(join(DOWNLOADS_PATH, file_name), "rb") as download:
                descargab64 = base64.b64encode(download.read())
            os.remove(join(DOWNLOADS_PATH, file_name))
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                             payload={"zip descargado": str(descargab64)})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            self.logout()
            log_prod.info(f"job= {self._id}|END OF PROCESS")
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def liquidacion_mensual(self, t_s: float = None, headless: bool = None, t_o: float = None):
        try:
            t_o = self.t_o if not t_o else t_o
            t_s = self.t_s if not t_s else t_s
            t_o = dpath(self.config, "scrapper.arba.iibb.liquidacion_mensual.t_o", t_o)
            t_s = dpath(self.config, "scrapper.arba.iibb.liquidacion_mensual.t_s", t_s)
            headless = dpath(self.config, "scrapper.arba.iibb.liquidacion_mensual.headless", headless)
            self.run(headless=headless, t_o=t_o, t_s=t_s, c_d=True)
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            self.force_find_xpath(browser=self.browser, xpath=XPATH_IIBB_PRES_DDJJ, click=True)
            wait = WebDriverWait(self.browser, 20)
            wait.until(EC.number_of_windows_to_be(2))
            self.actual_window_2(browser=self.browser, from_id=[self.browser.current_window_handle], n_windows_end=2)
            self.wait_and_go(xpath=XPATH_IIBB_LIQUIDACION, click=True)
            self.wait_and_go(xpath=XPATH_IIBB_LIQUIDACION_OBLIGA, click=True)
            self.wait_and_go(xpath=XPATH_IIBB_OBLIG_PEST)
            select_anio_desde = self.wait_and_go(xpath=XPATH_IIBB_OBLIG_SELECT_ANIO_DESDE, click=False)
            select_anio_hasta = self.wait_and_go(xpath=XPATH_IIBB_OBLIG_SELECT_ANIO_HASTA, click=False)
            select_mes_desde = self.wait_and_go(xpath=XPATH_IIBB_OBLIG_SELECT_MES_DESDE, click=False)
            select_mes_hasta = self.wait_and_go(xpath=XPATH_IIBB_OBLIG_SELECT_MES_HASTA, click=False)
            select_anio_desde = Select(select_anio_desde)
            select_anio_hasta = Select(select_anio_hasta)
            select_mes_desde = Select(select_mes_desde)
            select_mes_hasta = Select(select_mes_hasta)
            select_anio_desde.select_by_visible_text(str(self.data["payload"]["anio"]))
            select_anio_hasta.select_by_visible_text(str(self.data["payload"]["anio"]))
            select_mes_desde.select_by_visible_text(str(self.data["payload"]["mes/bimestre"]))
            select_mes_hasta.select_by_visible_text(str(self.data["payload"]["mes/bimestre"]))
            self.wait_and_go(xpath=XPATH_IIBB_OBLIGACION_BUSCAR, click=True)
            self.wait_and_go(xpath=XPATH_IIBB_OBLIGACION_VER, click=True)
            self.wait_and_go(xpath=XPATH_IIBB_PRES_DDJJ_RESUMEN, click=True)
            name = "resumen"
            sfx1 = self.data["payload"]["anio"]
            sfx2 = self.data["payload"]["mes/bimestre"]
            sfx2 = sfx2 if len(sfx2) == 2 else "0" + str(sfx2)
            name = name + str(sfx1) + str(sfx2)
            time.sleep(5)
            tmp = "/tmp/"
            patron = re.compile(name.upper())
            download = None
            for x in listdir(join(tmp, str(self._id))):
                if re.search(patron, x.upper()):
                    with open(join(tmp, str(self._id), x), "rb") as f:
                        download = base64.b64encode(f.read())
                    os.remove(join(tmp, str(self._id), x))
            if not download:
                log_prod.error("El resumen descargado no pude ser localizado")
                raise FileNotFoundError("El resumen descargado no pude ser localizado")
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                             payload={"pdf liquidación presentada": str(download)})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            self.logout()
            log_prod.info(f"job= {self._id}|END OF PROCESS")
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)


if __name__ == "__main__":
    from factory.servicios_varios import *
    from pprint import pprint
    a = IIBB(**liquidacion_mensual)
    d = a.liquidacion_mensual()
    print(d)
