from anfler_base.anfler_baseclass import BaseClass, log_prod, log_dev
from anfler_afip.anfler_login import Login
from anfler_afip.settings import *
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from anfler.util.msg import message as msg
import time
from datetime import datetime, timedelta
from anfler.util.helper import dpath
from anfler_afip.anfler_tasks import create_task, update_task



class CCMA(BaseClass):
    """Clase login para acceso a seccion monotributo AFIP"""

    def __init__(self, message: (dict, str), xpaths: tuple = C_XPATHS_CCMA, browser="chrome",
                 t_s: float = 0.5, options: bool = True, *args, **kwargs):
        """
        :param message: json or dict with information 'cuit', 'password' in the key 'data'
        :param pwd: str contraseña de acceso del contribuyente
        :param pwd: tuple contiene 5 rutas de recorrido basico al destino en el siguiente orden
                    (XPATH_USERNAME, X_PATH_PASSWORD, XPATH_CCMA, XPATH_CALCULO_DEUDA, XPATH_BODY_DEUDA)
        """
        super(CCMA, self).__init__(browser=browser)  # por default la BaseClass corre chrome
        log_prod.info("INSTANCING CCMA CLASS")
        self.data = self.validate_message(message)
        cuit, pwd = self.extract_cuit_pwd(self.data)
        self.cuit, self.pwd = self.validate(cuit, pwd)
        self.xpaths = {'xpaths_login': xpaths[0:2], 'xpaths_ccma': xpaths[2:]}
        self.browser = dpath(self.config, "scrapper.afip.ccma.browser", browser)
        self.t_s = dpath(self.config, "scrapper.afip.ccma.t_s", t_s)
        self.options = dpath(self.config, "scrapper.afip.ccma.options", options)
        self.headless = dpath(self.config, "scrapper.afip.ccma.headless", True)
        self._id = self.data["id"]

    def run(self, t_s: float = 2, t_o: float = None, headless: bool = None):
        try:            
            # SE CREA INSTANCIA EN LA BASE DE DATOS TASK.PY
            create_task(job_id=self._id,
                        servicio='ccma',
                        task_status="init-not-end",
                        task_error='not-error')
            
            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.ccma.run.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.ccma.run.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.ccma.run.headless", headless)
            self.browser = Login(cuit=self.cuit,
                                 pwd=self.pwd,
                                 browser=self.browser,
                                 t_o=t_o,
                                 id_=self._id).run(self.xpaths['xpaths_login'],
                                                   options=self.options,
                                                   headless=headless)
            time.sleep(t_s)
            if not self.validate_browser(self.browser):
                # raise SessionNotCreatedException(self.browser)
                raise Exception(self.browser)
            wait = WebDriverWait(self.browser, 20)
            if self.browser.current_url == URL1 or self.browser.current_url == URL0:
                log_prod.debug("=======================URL 1=====================")
                search = self.force_find_xpath(browser=self.browser, xpath=XPATH_CAJAS_AFIP, max_r=30,
                                               t_s=t_s, group=True, name=NAME_CCMA)
                if isinstance(search, AssertionError):
                    raise search
            elif self.browser.current_url == URL2:
                log_prod.debug("=======================URL 2=====================")
                search = self.force_find_xpath(self.browser, XPATH_LISTA_URL_2, t_s=t_s, click=True,
                                               group=True, name=NAME_CCMA)
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
                                                    name=NAME_CCMA )
                    log_prod.info(f" job= {self._id} | SE ENCONTRO LA CAJA CCMA" )
                    print('se encontro la caja')
                    
                    self.browser.execute_script("arguments[0].scrollIntoView(true);", search)
                    time.sleep(1)
                    search.click()

                except:
                   
                    log_prod.error(f"job= {self._id} | NO SE ENCONTRO LA CAJA CCMA")
                    print('no se encontro la caja')
                    input_element = self.force_find_xpath(browser=self.browser, xpath="/html/body/div/div/main/div/section/div/div[2]/div/div[1]/div/div/div[1]/input", t_s=5)
                    input_element.send_keys('CCMA - CUENTA CORRIENTE DE CONTRIBUYENTES MONOTRIBUTISTAS Y AUTONOMOS')
                    time.sleep(1)
                    modal_element = self.force_find_xpath(browser=self.browser, 
                                                          xpath="/html/body/div/div/main/div/section/div/div[2]/div/div[1]/div/div/ul/li/a/div/div/div[2]/button", 
                                                          t_s=5, 
                                                          click=True,
                                                          name= 'Agregar')
                    log_prod.info(f"job= {self._id} | SE AGREGO CAJA NUEVA CCMA Y SE ACCEDIO A ELLA ")
                    time.sleep(1)    

                    #if isinstance(search, AssertionError):
                    #    raise search

            else:
                raise NoSuchWindowException("Se accedio a una ruta desconocida")
            time.sleep(t_s)
            wait.until(EC.number_of_windows_to_be(2), message=f"Esperando que se cree la ventana 2")
            windows = self.browser.window_handles
            self.browser.switch_to.window(windows[1])
            wait = WebDriverWait(self.browser, 20)
            self.browser.set_window_size(1920, 1080)
            XPATH_BOTON_SELECT_CUIT_CCMA = "/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div[2]/form/div[2]/input"
            boton_select_ = self.browser.find_elements_by_xpath(XPATH_BOTON_SELECT_CUIT_CCMA)
            if len(boton_select_) > 0:
                boton_select_[0].click()
            time.sleep(2)
            if "P02_ctacte".upper() not in str(self.browser.current_url).upper():
                text = self.browser.find_elements_by_xpath("/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/div/b[1]/font")
                if len(text) > 0:
                    resumen = text[0].text
                    response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]},
                                                     payload={"message": resumen})
                    response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
                    self.browser.quit()
                    log_prod.info(f"job= {self._id}|END OF PROCESS")

                    # SE ACTUALIZA REGISTRO EN BASE DE DATOS TASK.PY TAREA EXITOSA
                    update_task(job_id=self._id,
                                task_status="end-successful",
                                task_error="not error")

                    return response
                
                raise NotImplementedError("La pagina CCMA no esta disponible en este momento para el usuario indicado")
           
           
            wait.until(EC.element_to_be_clickable((By.XPATH, self.xpaths['xpaths_ccma'][1])),
                       message=f"Esperando por: " + inv_xpath.get(self.xpaths['xpaths_ccma'][1],
                                                                  self.xpaths['xpaths_ccma'][1]))
            XPATH_FROM = "/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/form/table/tbody/tr[1]/td[2]/div/input"
            XPATH_TO = "/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/form/table/tbody/tr[2]/td[2]/div/input"
            desde = self.wait_and_go(xpath=XPATH_FROM, click=False)
            hasta = self.wait_and_go(xpath=XPATH_TO, click=False)
            desde.clear()
            hasta.clear()
            def validate_data(data: str):
                length = bool(len(data) == 7)
                numbers = data.split("/")
                numbers = all([x.isdigit() for x in numbers])
                month = bool(0 < int(data[:2]) <= 12)
                return all([length, numbers, month])
            if self.data['payload'].get("from", False) and self.data['payload'].get("to", False):
                valid_from = validate_data(self.data['payload']["from"])
                valid_to = validate_data(self.data['payload']["to"])
                if not all([valid_from, valid_to]):
                    raise KeyError("No se pudo validar el formato de las fechas, esperado: mm/yyyy")
                desde.send_keys(self.data['payload']['from'])
                hasta.send_keys(self.data['payload']['to'])
            else:
                today = datetime.utcnow()
                ten_years = today - timedelta(days=10*365)
                desde.send_keys(str(today.month).zfill(2) + "/" + str(today.year - 10))
                hasta.send_keys(str(today.month).zfill(2) + "/" + str(today.year))

            self.force_find_xpath(browser=self.browser, xpath=self.xpaths['xpaths_ccma'][1], t_s=t_s)

            wait.until(EC.element_to_be_clickable((By.XPATH, self.xpaths['xpaths_ccma'][2])),
                       message=f"Esperando por: " + inv_xpath.get(self.xpaths['xpaths_ccma'][2],
                                                                  self.xpaths['xpaths_ccma'][2]))
            resumen = self.force_find_xpath(browser=self.browser, xpath=self.xpaths['xpaths_ccma'][2],
                                            click=False, t_s=t_s)
            resumen = resumen.text
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]}, payload={"resumen": resumen})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            self.browser.quit()
            log_prod.info(f"job= {self._id}|END OF PROCESS")

            # SE ACTUALIZA REGISTRO EN BASE DE DATOS TASK.PY COMO TAREA EXITOSA
            update_task(job_id=self._id,
                        task_status="end-successful",
                        task_error="not-error")
            
            return response
        
        except (WebDriverException, Exception) as e:

             # SE ACTUALIZA REGISTRO EN BASE DE DATOS TASK.PY COMO TAREA FALLIDA
            update_task(job_id=self._id,
                        task_status="failed",
                        task_error=e)
            
            return self.return_exception(self.browser, self.data, e)


if __name__ == "__main__":
    ccma = {
        'message': {
            'status': 0,
            'errors': [],
            'id': '1234567890',
            'header': {
                'auth': {
                    'codif': 0,
                    'cuit': 1,
                    'password': "5",
                    'type': 'basic'
                },
                "method_args": {"headless": True},
                'job_service': "afip",
                'fn': 'anfler_afip.anfler_ccma.CCMA@run',
                'key': None,
                'offset': 0,
                'partition': 0
            },
            'payload': {
            },
        },
        "browser": "chrome"
    }
    a = CCMA(**ccma).run()
    print(a)
