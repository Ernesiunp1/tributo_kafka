import random
from anfler_base.anfler_baseclass import BaseClass, log_prod
from anfler_afip.anfler_login import Login
from anfler_afip.settings import *
from selenium.common.exceptions import *
import time
from anfler.util.msg import message as msg
from anfler.util.helper import dpath
from selenium.webdriver.support.ui import WebDriverWait
from anfler_afip.anfler_tasks import create_task, update_task


min_time = 2
max_time = 7
wait_time = random.uniform(min_time, max_time)


class SIPER(BaseClass):

    def __init__(self, message: (dict, str), t_s: float = 0.5, browser: str = "chrome", options: bool = True):

        super(SIPER, self).__init__()
        log_prod.info(f"job= {self._id} |==========INSTANCING SIPER ===========")
        time.sleep(random.choice(range(2, 13)))
        self.data = self.validate_message(message)
        cuit, pwd = self.extract_cuit_pwd(self.data)
        self.cuit, self.pwd = self.validate(cuit, pwd)
        self._id = self.data["id"]
        self.browser = dpath(self.config, "scrapper.afip.mis_comprobantes.browser", browser)
        self.options = dpath(self.config, "scrapper.afip.mis_comprobantes.options", options)
        self.t_s = dpath(self.config, "scrapper.afip.mis_comprobantes.t_s", t_s)
        self.headless = dpath(self.config, "scrapper.afip.mis_comprobantes.headless", True)

    def run(self, t_s: float = None, t_o: float = None):
        global motivo, fecha, extra_info
        riesgo = {}
        wait_ = WebDriverWait(self.browser, 60)        
        log_prod.info(f"job= {self._id} |GOING TO PERFIL DE RIESGO")

        try:
            # SE CREA INSTANCIA EN LA BASE DE DATOS TASK.PY
            create_task(job_id=self._id,
                        servicio='ccma',
                        task_status="init-not-end",
                        task_error='not-error')
            

            self.browser = Login(browser=self.browser,
                                 cuit=self.cuit,
                                 pwd=self.pwd,
                                 id_=self._id,
                                 change_dir=False).run(xpath=C_XPATHS_LOGIN,
                                                       t_s=t_s,
                                                       options=self.options,
                                                       headless=True,
                                                       t_o=t_o)

            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)

            self.browser.maximize_window()
            WebDriverWait(self.browser, 60)

            if self.browser.current_url == URL3:
                log_prod.debug(f"job= {self._id} |=======================URL 3=====================")
                print('Estamos en URL3')
                time.sleep(wait_time)

                #  SE AGREGA DE FORMA AUTOMATICA
                log_prod.warning(f"job= {self._id} | TRYING BUSCADOR EN VER TODOS")

                xpath_buscador = "/html/body/div/div/main/div/section/div/div[2]/div/div[1]/div/div/div[1]/input"
                input_element = self.force_find_xpath(browser=self.browser,
                                                      xpath=xpath_buscador,
                                                      t_s=5)

                input_element.send_keys('Sistema registral Altas bajas')
                log_prod.warning(f"job= {self._id} | INTRODUCIENDO SISTEMA REGISTRAL EN BUSCADOR")

                time.sleep(wait_time)
                xpath_modal = "/html/body/div/div/main/div/section/div/div[2]/div/div[1]/div/div/ul/li[1]/a"
                self.force_find_xpath(browser=self.browser,
                                      xpath=xpath_modal,
                                      t_s=5,
                                      click=True,
                                      name='Agregar')

                time.sleep(10)
                log_prod.info(f"job= {self._id} | SE AGREGO CAJA SISTEMA REGISTRAL")

                # CAMBIANDO EL DRIVER DE VENTANA
                ventanas = self.browser.window_handles
                self.browser.switch_to.window(ventanas[1])
                time.sleep(5)

                ################################################################
                #       AQUI ESTAMOS A NIVEL DEL MENU DE TRAMITES (ASIDE)      #
                ################################################################

                try:
                    log_prod.warning(f"job= {self._id} | FROM SIPER | BUSCANDO SI HAY MAS DE UN USUARIO")
                    self.browser.find_element_by_xpath(
                        "//div[@class='selPersona unit-100']/h3[@style='font-weight: bold;']")
                    log_prod.warning(f"job= {self._id} | FROM SIPER | SELECCIONANDO PERSONA A REVISAR")
                    self.browser.find_element_by_xpath("/html/body/div[1]/div/form/div[2]").click()
                    log_prod.warning(f"job= {self._id} | FROM SIPER | CLICK EN PERSONA SELECCIONADA: OK")
                    time.sleep(wait_time)
                except Exception as e:
                    log_prod.warning(f"job={self._id} | FROM SIPER | SALIENDO DE CASO 2 | VARIOS USUARIOS TS " )

                # ACCESANDO A LA LISTA TRAMITES Y BOTON VER RIESGO
                time.sleep(wait_time)
                self.acceso_riesgos()

                # EXTRAYENDO LOS DATOS DE TRAJETA DE RIESGO
                time.sleep(wait_time)
                riesgo = self.extraccion_datos_siper()

                # PREPARANDO RESPUESTA
                response = msg.get_basic_message()
                response = msg.update_message(response,
                                              header={"fn": self.data["header"]["fn"]},
                                              id=self.data["id"],
                                              status=STATUS_OK,
                                              payload={"siper": riesgo})
                self.logout()
                log_prod.warning(
                    f'job= {self._id} | FROM SIPER | FINALIZANDO PROCESO | RESPUESTA ENVIADA')
                
                # SE ACTUALIZA REGISTRO EN BASE DE DATOS TASK.PY COMO TAREA EXITOSA
                update_task(job_id=self._id,
                        task_status="end-successful",
                        task_error="not-error")
                
                
                return response

        except Exception as e:
            
            # SE ACTUALIZA REGISTRO EN BASE DE DATOS TASK.PY COMO TAREA FALLIDA
            update_task(job_id=self._id,
                        task_status="failed",
                        task_error=e)
            
            return self.return_exception(self.browser, self.data, e)


if __name__ == "__main__":
    cuit= 2
    password=  'A4'
    siper = {
        'message': {
            'status': 0,
            'errors': [],
            'id': '1234567890',
            'header': {
                'auth': {
                    'codif': 0,
                    'cuit':     cuit,       
                    'password': password,    
                    'type': 'basic'
                },
                "method_args": {"headless": True},
                'job_service': "afip",
                'fn': 'anfler_afip.anfler_siper.SIPER@run',
                'key': None,
                'offset': 0,
                'partition': 0
            },
            'payload': {
            },
        },
        "browser": "chrome"
    }
    a = SIPER(**siper).run()
    print(a)

