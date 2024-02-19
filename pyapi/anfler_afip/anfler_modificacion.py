from anfler_base.anfler_baseclass import BaseClass, log_prod
from anfler_afip.settings import *
from anfler_afip.anfler_login import Login
from anfler.util.msg import message as msg
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException, NoSuchWindowException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time


class Modificacion(BaseClass):

    def __init__(self, message: str, browser: str = "chrome", t_s: float = 2, options: bool = True, *args, **kwargs):
        super(Modificacion, self).__init__()
        log_prod.info(f"job= {self._id}| ==================INSTANCING CLASS MODIFICACION====================")
        self.data = self.validate_message(message)
        cuit, pwd = self.extract_cuit_pwd(self.data)
        self.cuit, self.pwd = self.validate(cuit, pwd)
        self.browser = dpath(self.config, "scrapper.afip.modificacion.browser", browser)
        self.t_s = dpath(self.config, "scrapper.afip.modificacion.t_s", t_s)
        self.options = dpath(self.config, "scrapper.afip.modificacion.options", options)
        self.headless = dpath(self.config, "scrapper.afip.modificacion.headless", False)
        self._id = self.data["id"]

    def run(self, t_s: float = 1, t_o: float = None, headless: bool = None):
        log_prod.info("START BROWSER TO CERTIFICATE")
        try:
            self.browser = Login(self.cuit,
                                 self.pwd,
                                 browser=self.browser,
                                 t_o=t_o, id_=self._id).run(C_XPATHS_LOGIN,
                                                            t_s=t_s,
                                                            options=self.options,
                                                            headless=True)
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            self.browser.set_window_size(width=1980, height=1020)
            if self.browser.current_url == URL1 or self.browser.current_url == URL0:
                log_prod.debug("=======================URL 1=====================")
                search = self.force_find_xpath(browser=self.browser, xpath=XPATH_CAJAS_AFIP, max_r=30,
                                               t_s=t_s, group=True, name=NAME_MONOTRIBUTO)
                if isinstance(search, AssertionError):
                    raise search
            elif self.browser.current_url == URL2:
                log_prod.debug("=======================URL 2=====================")
                search = self.force_find_xpath(self.browser, XPATH_LISTA_URL_2, t_s=t_s, click=True,
                                               group=True, name=NAME_MONOTRIBUTO_LISTA)
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
            self.browser.get("https://monotributo.afip.gob.ar/app/DatosMonotributo.aspx")
            return self
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def modificar(self, t_s: float = 1, headless: bool = None, t_o: float = None):
        log_prod.info("=============Modificando Monotributo AFIP===============")
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.modificacion.modificar.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.modificacion.modificar.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.modificacion.modificar.headless", headless)
            self.run(t_s=t_s, headless=headless, t_o=t_o)
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            self.get_status_200(self.browser)
            wait = WebDriverWait(self.browser, t_o)
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BUTONS_MODIFICAR)))
            self.force_find_xpath(browser=self.browser,
                                  xpath=XPATH_BUTONS_MODIFICAR,
                                  group=True,
                                  name=NAME_MODIFICAR)
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_MODIFICAR_MIS_DATOS)))
            self.force_find_xpath(browser=self.browser, xpath=XPATH_MODIFICAR_MIS_DATOS)
            texto = self.step_4_5(self.step_3(self.step_2(self.step_1(self.browser, wait), wait), wait), wait)
            if isinstance(texto, KeyError):
                raise texto
            if isinstance(texto, Exception):
                raise texto
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]}, payload={"resumen": texto})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def step_1(self, browser, wait):
        log_prod.info(f"job= {self._id}|=============STEP 1 MODIFICACION==============")
        try:
            if isinstance(browser, KeyError):
                return browser
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_RADIO_MODIF_INDEP)))
            como_vas_a_trabajar = self.data["payload"].get("como_vas_a_trabajar", False)
            print("A TRABAJAR", como_vas_a_trabajar)
            if como_vas_a_trabajar:
                if como_vas_a_trabajar.upper() == "VOY A REALIZAR TRABAJO INDEPENDIENTE":
                    self.force_find_xpath(browser=browser, xpath=XPATH_RADIO_MODIF_INDEP)
                elif como_vas_a_trabajar.upper() == "COMO MIEMBRO DE UNA COOPERATIVA":
                    self.force_find_xpath(browser=browser, xpath=XPATH_RADIO_MODIF_COOP)
                elif como_vas_a_trabajar.upper() == "COMO TRABAJADOR PROMOVIDO":
                    self.force_find_xpath(browser=browser, xpath=XPATH_RADIO_MODIF_PROM)
                else:
                    raise Exception("El dato suministrado para el paso 1 no existe en la pagina")
            else:
                raise Exception("No se suministro el dato para es paso 1")
            self.force_find_xpath(browser=browser, xpath=XPATH_MOD_BUTON_SIGU)
            XPATH_DANGER = "//*[@id='divMensajeError']"
            time.sleep(2)
            mensajes = self.browser.find_elements_by_xpath(XPATH_DANGER)
            if len(mensajes) > 0:
                if len(mensajes[0].text) > 0:
                    return KeyError(mensajes[0].text)
            return browser
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def step_2(self, browser, wait, alta=False):
        log_prod.info(f"job= {self._id}|=============STEP 2 MODIFICACION==============")
        try:
            if isinstance(browser, KeyError):
                return browser
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_MOD_RADIO_STP2_ACTUAL)))
            mes_aplicacion = self.data["payload"].get("mes_aplicacion", False)
            if mes_aplicacion.upper() == "ACTUAL":
                self.force_find_xpath(browser=browser, xpath=XPATH_MOD_RADIO_STP2_ACTUAL)
            elif mes_aplicacion.upper() == "PROXIMO":
                self.force_find_xpath(browser=browser, xpath=XPATH_MOD_RADIO_STP2_PROX)
            else:
                log_prod.error(f"job= {self._id}| mes de aplicacion suministrado en STEP 2 MODIFICACION no existe")
            if self.data["payload"].get("facturacion_anual", False):
                buton_new = "/html/body/form/main/section[2]/div/div/div/div[2]/div[2]/div[1]/div/input[2]"
                form1 = self.force_find_xpath(browser=browser, xpath=XPATH_MOD_FORM_STP2_FACT_ANUAL)
                form1.clear()
                form1.send_keys(str(int(self.data["payload"]["facturacion_anual"])))
                buton_new = self.browser.find_elements_by_xpath(buton_new)
                if len(buton_new) > 0: buton_new[0].click()
            else:
                log_prod.info(f"job= {self._id}| Dato no suministrado: Facturacion Anual. STEP 2 MODIFICACION")
            usa_local = self.data["payload"].get("local", False)
            if usa_local.upper() == "SI":
                self.force_find_xpath(browser=browser, xpath=XPATH_MOD_FORM_STP2_RADIO_LOCAL_SI)
                kw = self.data["payload"].get("consumo_anual_energia", False)
                sup = self.data["payload"].get("superficie_afectada", False)
                if alta:
                    kw = True
                if sup and kw:
                    if not alta:
                        kw_ = self.force_find_xpath(browser=browser, xpath=XPATH_MOD_STP2_ENER_ANUAL)
                        kw_.send_keys(str(int(kw)))
                    sup_ = self.force_find_xpath(browser=browser, xpath=XPATH_MOD_STP2_FORM_SUP_AFEC)
                    sup_.send_keys(str(int(sup)))
                    alquilado = self.data["payload"].get("alquilado", False)
                    print("->", alquilado)
                    if alquilado.upper() == 'SI':
                        if alta:
                            XPATH_MOD_STP2_RADIO_LOC_ALQ_SI = "//*[@id='collapseMoreInfo1']/div[1]/div/input[1]"
                        print("aqui")
                        self.wait_and_go(xpath=XPATH_MOD_STP2_RADIO_LOC_ALQ_SI, click=True)
                        print("alla")
                        # self.force_find_xpath(browser=browser, xpath=XPATH_MOD_STP2_RADIO_LOC_ALQ_SI)
                        alquiler = self.wait_and_go(xpath=XPATH_MOD_STP2_FORM_MONTO_ALQ, click=False)
                        # alquiler = self.force_find_xpath(browser=browser, xpath=XPATH_MOD_STP2_FORM_MONTO_ALQ)
                        alquiler.send_keys(str(int(self.data["payload"]["monto_anual_alquiler"])))
                else:
                    log_prod.error(f"job= {self._id}|=>No fueron suministrados los datos correspondientes a KW y m2<=")
            elif usa_local.upper() == "NO":
                self.force_find_xpath(browser=browser, xpath=XPATH_MOD_FORM_STP2_RADIO_LOCAL_NO)
            else:
                log_prod.info(f"job= {self._id}| Dato no suministrado: Usa Local. STEP 2 MODIFICACION")
            self.force_find_xpath(browser=self.browser, xpath=XPATH_MOD_BUTON_SIGU_STP2, click=True)
            XPATH_DANGER = "//*[@id='divMensajeError']"
            time.sleep(2)
            mensajes = self.browser.find_elements_by_xpath(XPATH_DANGER)
            if len(mensajes) > 0:
                if len(mensajes[0].text) > 0:
                    return KeyError(mensajes[0].text)
            return browser
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def step_3(self, browser, wait, alta=False):
        log_prod.info(f"job= {self._id}|=============STEP 3 MODIFICACION==============")
        try:
            if isinstance(browser, KeyError):
                return browser
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_MOD_RADIO_STP3_ACT)))
            jubilacion = self.data["payload"].get("jubilacion", False)
            print(jubilacion)
            if jubilacion.upper() == "TRABAJADOR ACTIVO":
                self.force_find_xpath(browser=browser, xpath=XPATH_MOD_RADIO_STP3_ACT)
            elif jubilacion.upper() == "EMPLEADO EN RELACION DE DEPENDENCIA":
                print("llegue")
                self.wait_and_go(xpath=XPATH_MOD_RADIO_STP3_DEP, click=True)
                XPATH_VALIDAR = "//*[@id='btnValidarEmpleador']"
                validar = self.browser.find_elements_by_xpath(XPATH_VALIDAR)
                modificar = self.browser.find_elements_by_xpath(XPATH_MOD_BUTON_CAM_EMP)
                cuit = self.data["payload"].get("cuit_empleador", False)
                if not alta and modificar[0].is_displayed():
                    self.wait_and_go(xpath=XPATH_MOD_BUTON_CAM_EMP, click=True)
                if cuit:  # Si llega un cuit se supone cambio de empleador
                    # self.wait_and_go(xpath=XPATH_MOD_FORM_CAM_EMP, click=False)
                    cuit_nuevo = self.force_find_xpath(browser=browser, xpath=XPATH_MOD_FORM_CAM_EMP)
                    if alta:
                        cuit_nuevo.send_keys(str(cuit))
                        self.wait_and_go(xpath="//*[@id='btnValidarEmpleador']", click=True)
                    else:
                        cuit_nuevo.send_keys(str(cuit))  # + Keys.TAB + Keys.RETURN)
                        self.wait_and_go(xpath="//*[@id='btnValidarEmpleador']", click=True)
                    print("continuando e")
            elif jubilacion.upper() == "JUBILADO":
                self.force_find_xpath(browser=browser, xpath=XPATH_MOD_RADIO_STP3_JUBILADO)
                ley = self.data["payload"].get("ley", False)
                if ley == "24.241":
                    self.force_find_xpath(browser=browser, xpath=XPATH_MOD_RADIO_STP3_LEY_24241)
                elif ley == "18.038/8":
                    self.force_find_xpath(browser=browser, xpath=XPATH_MOD_RADIO_STP3_LEY_180388)
                else:
                    log_prod.error(f"job= {self._id}| Ley indicada no esta especificada en la web de AFIP")
                    raise ValueError("Ley indicada no esta especificada en la web de AFIP")
            elif jubilacion.upper() == "APORTO A UNA CAJA PREVISIONAL":
                self.force_find_xpath(browser=browser, xpath=XPATH_MOD_RADIO_STP3_CAJA)
                cuit = self.data["payload"].get("cuit_caja", False)
                if cuit:
                    cuit_ = self.force_find_xpath(browser=browser, xpath=XPATH_MOD_FORM_STP3_CAJ_CUIT)
                    cuit_.send_keys(str(cuit)+Keys.RETURN)
                else:
                    log_prod.error(f"job= {self._id}| CUIT CAJA en STEP 3 MODIFICACION no suministrado")
                    raise KeyError("EL dato de CUIT CAJA no fue suministrado adecuadamente")
            elif jubilacion.upper() == "LOCADOR DE BIENES MUEBLES O INMUEBLES":
                self.force_find_xpath(browser=browser, xpath=XPATH_MOD_RADIO_STP3_LOCADOR)
            else:
                log_prod.error(f"job= {self._id}| Jubilacion en STEP 3 MODIFICACION no existe")
                raise KeyError("EL dato de jubilación no coincide con los parametros esperados")
            self.wait_and_go(xpath=XPATH_MOD_BUTON_SIGU_STP3, click=True)
            time.sleep(1)
            XPATH_DANGER = "//*[@id='divMensajeError']"
            time.sleep(2)
            mensajes = self.browser.find_elements_by_xpath(XPATH_DANGER)
            if len(mensajes) > 0:
                if len(mensajes[0].text) > 0:
                    return KeyError(mensajes[0].text)
            return browser
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e, close=False)

    def step_4_5(self, browser, wait):
        log_prod.info(f"job= {self._id}|=============STEP 4 MODIFICACION==============")
        try:
            if isinstance(browser, KeyError):
                return browser
            if isinstance(browser, Exception):
                return browser
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_MOD_STP4)))
            # l = self.force_find_xpath(browser=browser, xpath=XPATH_MOD_STP4_YA_TIENE,
            #                          click=False, group=True, lista=True)
            time.sleep(5)
            l = self.browser.find_elements_by_xpath(XPATH_MOD_STP4_YA_TIENE)
            if len(l) == 0:
                tiene = False
            else:
                tiene = True
            if tiene:
                pass
            else:
                o_s = self.data["payload"].get("codigo_obra_social", False)
                aporte = self.data["payload"].get("sumar_aportes_de_conyuge", False)
                if o_s:
                    TEXT_SELECCIONE = "//*[@id='divPuedeElegirOS']/div[1]/label"
                    ID_OBRA_CHOOSE = "selObraSocial_chosen"
                    XPATH_SELECCIONE_OBRA = "/html/body/form/main/section[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div/input"
                    aux = "//*[@id='selObraSocial_chosen']/a/span"
                    h = self.browser.find_element_by_tag_name("html")
                    h.send_keys(Keys.END)
                    # place = self.wait_and_go(xpath=XPATH_SELECCIONE_OBRA, click=False)
                    time.sleep(5)
                    place = self.wait_and_go(xpath=TEXT_SELECCIONE)
                    ## place = place.location
                    # accion = ActionChains(self.browser)
                    # accion.move_to_element_with_offset(place, 20, 50).click().perform()
                    ## accion.move_to_element(place).click().perform()
                    # self.wait_and_go(xpath="//*[@id='selObraSocial_chosen']/a/span", click=True)
                    # self.force_find_xpath(browser=browser, xpath=XPATH_MOD_STP4_OS1)
                    choosing = self.browser.find_elements_by_id(ID_OBRA_CHOOSE)
                    if len(choosing) > 0:
                        choosing[0].click()
                    obra_social = self.force_find_xpath(browser=browser, xpath=XPATH_MOD_STP4_OS2)
                    # obra_social = self.wait_and_go(xpath=XPATH_MOD_STP4_OS2, click=True)
                    obra_social.send_keys(o_s + Keys.RETURN)
                    time.sleep(20)
                    if aporte.upper() == "NO":
                        self.force_find_xpath(browser=browser, xpath=XPATH_MOD_STP4_RADIO_APORTE_N)
                    elif aporte.upper() == "SI":
                        self.force_find_xpath(browser=browser, xpath=XPATH_MOD_STP4_RADIO_APORTE_S)
                        cuil_cony = self.force_find_xpath(browser=browser, xpath=XPATH_MOD_STP4_CUIL_CONY)
                        cuil_cony.send_keys(str(self.data["payload"]["cuil_conyuge"]) + Keys.TAB + Keys.RETURN)
                        self.force_find_xpath(browser=browser, xpath=XPATH_MOD_STP4_BTN_AGRE_CONY)
                    else:
                        log_prod.error(f"job= {self._id}| Se suministro un dato incompatible en el paso 4")
                if self.data["payload"].get("cuil_familiar_adicional", False):
                    for x in self.data["payload"]["cuil_familiar_adicional"]:
                        form = self.force_find_xpath(browser=browser, xpath=XPATH_MOD_STP4_FORM_CUIL_FAM)
                        form.send_keys(str(x[0]) + Keys.TAB + Keys.RETURN)
                        select = self.force_find_xpath(browser=browser, xpath=XPATH_MOD_STP4_SELECT_AGRE_FAM)
                        select = Select(select)
                        select.select_by_visible_text(x[1])
                        self.force_find_xpath(browser=browser, xpath=XPATH_MOD_STP4_BTN_AGRE_FAM)
                self.wait_and_go(xpath=XPATH_MOD_STP4_CHKBX_SIPA, click=True)
            self.wait_and_go(xpath=XPATH_MOD_STP4_CONT, click=True)
            provincial = self.data["payload"].get("componente_provincial", False)
            mas_de_una = self.data["payload"].get("actividad en mas de una provincia", False)
            if provincial or mas_de_una:
                mas_de_una = self.data["payload"]["actividad en mas de una provincia"]
                if mas_de_una.upper() == "SI":
                    self.wait_and_go(xpath="//*[@id='divConvenio']/div/input[1]", click=True)
                elif mas_de_una.upper() == "NO":
                    time.sleep(2)
                    mas = self.browser.find_elements_by_xpath("//*[@id='divConvenio']/div/input[2]")
                    if len(mas) > 0:
                        self.wait_and_go(xpath="//*[@id='divConvenio']/div/input[2]", click=True)
                self.wait_and_go(xpath="//*[@id='btnSiguiente']", click=True)
            time.sleep(2)
            response = self.force_find_xpath(browser=browser, xpath=XPATH_MOD_STP5_RESUMEN)
            response = response.text
            self.force_find_xpath(browser=browser, xpath=XPATH_MOD_STP4_CONFIRMAR)
            self.logout()
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def baja(self, t_s: float = 1, headless: bool = None, t_o: float = None):
        log_prod.info("=============Modificando Monotributo AFIP===============")
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.modificacion.baja.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.modificacion.baja.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.modificacion.baja.headless", headless)
            self.run(t_s=t_s, headless=headless, t_o=t_o)
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            self.get_status_200(self.browser)
            wait = WebDriverWait(self.browser, t_o)
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BUTONS_MODIFICAR)))
            self.browser.get("https://monotributo.afip.gob.ar/app/Baja.aspx")
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_CALENDARIO_BAJA)))
            calendar_ = self.find_xpath(self.browser, XPATH_CALENDARIO_BAJA, click=True)
            calendar_.send_keys(str(self.data["payload"]["periodo"]) + Keys.TAB)
            modo_baja = self.data["payload"]["modo_baja"]
            xpath_modo = DICT_XPATH_BAJA.get(modo_baja.upper(), False)
            if xpath_modo:
                self.find_xpath(self.browser, xpath_modo, click=True)
            else:
                log_prod.error(f"El modo de baja {modo_baja} no disponible")
                raise KeyError(f"El modo de baja {modo_baja} no disponible")
            self.force_find_xpath(self.browser, XPATH_BAJA_MON_CONTI, click=True)
            actuales = self.browser.window_handles
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BAJA_GO_RUT)))
            self.force_find_xpath(self.browser, XPATH_BAJA_GO_RUT, click=True)
            nuevas = self.browser.window_handles
            for x in nuevas:
                if x not in actuales:
                    self.browser.switch_to.window(x)
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BAJA_CONFIRMAR_IMP)))
            boton = self.force_find_xpath(self.browser, XPATH_BAJA_CONFIRMAR_IMP, click=False)
            texto = boton.text
            # boton.click()
            if texto.upper() == "CONFIRMAR":
                r = "Baja Confirmada"
            else:
                r = "No se pudo confirmar la baja completamente, por favor verifique manualmente o vuelva a intentar"
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]}, payload={"respuesta": r})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)

    def alta(self, t_s: float = 1, headless: bool = None, t_o: float = None):
        log_prod.info("=============Modificando Monotributo AFIP===============")
        try:
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.modificacion.alta.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.modificacion.alta.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.modificacion.alta.headless", headless)
            self.run(t_s=t_s, headless=headless, t_o=t_o)
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            self.get_status_200(self.browser)
            self.wait_and_go(xpath=XPATH_VER_CONSTANCIA, click=False)
            self.force_find_xpath(browser=self.browser, xpath=XPATH_VER_CONSTANCIA, group=True,
                                  name="Darse de Alta".upper(), click=True)
            wait = WebDriverWait(self.browser, t_o)
            texto = self.step_4_5(self.step_3(self.step_2(self.step_1(self.browser, wait), wait, alta=True), wait,
                                              alta=True), wait)
            if isinstance(texto, KeyError):
                raise texto
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]}, payload={"resumen": str(texto)})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            return response
        except (WebDriverException, Exception) as e:
            return self.return_exception(self.browser, self.data, e)


if __name__ == "__main__":
    from test_recategorizacion import modificacion
    from factory.servicios_varios import alta_monotributo, modificacion_kevin, alta_monotributo_simplificado, modificacion
    # a = Modificacion(**alta_monotributo_simplificado).alta()
    a = Modificacion(**modificacion).modificar()
    print(a)