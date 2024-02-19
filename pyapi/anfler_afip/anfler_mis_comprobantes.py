import random
import re

from anfler_base.anfler_baseclass import BaseClass, log_prod
from anfler_afip.anfler_login import Login
from anfler_afip.settings import *
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
import time
from anfler.util.msg import message as msg
from anfler.util.helper import dpath
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from peewee import *
import datetime
from os.path import exists
from anfler_afip.anfler_queue import AnflerQueue

from anfler_afip.anfler_tasks import create_task, update_task
from exceptions.exceptions import ExceptionResultados


def create_db(db_name):

    DATABASE = SqliteDatabase(db_name)

    class BaseModel(Model):
        class Meta:
            database = DATABASE

    class User(BaseModel):
        user_cuit = IntegerField(unique=True)

    class Service(BaseModel):
        user = ForeignKeyField(User, backref='service')
        job_id = CharField()
        created_date = DateTimeField(default=datetime.datetime.now)
        finished = BooleanField(default=False)
        service_name = CharField()

    if not exists(db_name):
        DATABASE.connect()
        DATABASE.create_tables([User, Service])
        DATABASE.commit()
        DATABASE.close()
    return User, Service


class MisComprobantes(BaseClass):

    def __init__(self, message: (dict, str), t_s: float = 0.5, browser: str = "chrome", options: bool = True):
        super(MisComprobantes, self).__init__()
        log_prod.info(f"job= {self._id} |==========INSTANCING MIS COMPROBANTES==========")
        time.sleep(random.choice(range(2, 13)))
        self.data = self.validate_message(message)
        cuit, pwd = self.extract_cuit_pwd(self.data)
        self.cuit, self.pwd = self.validate(cuit, pwd)
        self._id = self.data["id"]
        self.browser = dpath(self.config, "scrapper.afip.mis_comprobantes.browser", browser)
        self.options = dpath(self.config, "scrapper.afip.mis_comprobantes.options", options)
        self.t_s = dpath(self.config, "scrapper.afip.mis_comprobantes.t_s", t_s)
        self.headless = dpath(self.config, "scrapper.afip.mis_comprobantes.headless", True)

        db_name = f'/tmp/{self.cuit}.db'
        self.user, self.service = create_db(db_name)
        self.queue = AnflerQueue(self.user, self.service)

    def run(self, t_s: float = None, headless: bool = True, t_o: float = None):
        log_prod.info(f"job= {self._id} |GOING TO 'COMPROBANTES'")

        
        try:
            self.browser = Login(browser=self.browser,
                                 cuit=self.cuit,
                                 pwd=self.pwd,
                                 id_=self._id,
                                 change_dir=False).run(xpath=C_XPATHS_LOGIN,
                                                       t_s=t_s,
                                                       options=self.options,
                                                       headless=headless,
                                                       t_o=t_o)

            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)

            self.browser.maximize_window()

            wait_ = WebDriverWait(self.browser, 60)

            if self.browser.current_url == URL1 or self.browser.current_url == URL0:
                log_prod.debug(f"job= {self._id} |=======================URL 1=====================")

                time.sleep(10)
                search = self.force_find_xpath(self.browser,
                                               xpath=XPATH_CAJAS_AFIP,
                                               t_s=t_s,
                                               click=True,
                                               group=True,
                                               name=NAME_MIS_COM)

                if isinstance(search, AssertionError):
                    raise search

            elif self.browser.current_url == URL2:
                log_prod.debug(f"job= {self._id} |=======================URL 2=====================")
                wait_.until(EC.element_to_be_clickable((By.XPATH, XPATH_GROUP_URL2)))
                search = self.force_find_xpath(self.browser,
                                               XPATH_LISTA_URL_2,
                                               t_s=t_s,
                                               click=True,
                                               group=True,
                                               name=NAME_MIS_COM)
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
                                                    name=NAME_MIS_COM )
                    log_prod.info(f"job= {self._id} | SE ENCONTRO LA CAJA MIS_COMP")
                    print('se encontro la caja')
                    
                    self.browser.execute_script("arguments[0].scrollIntoView(true);", search)
                    time.sleep(1)
                    search.click()
                    time.sleep(t_s)

                    w_id = self.browser.current_window_handle

                    log_prod.info(f"job= {self._id} |w_id: {w_id}")

                    self.actual_window_2(self.browser, from_id=[w_id], n_windows_end=2, t_s=t_s)

                    return self

                except:
                    
                    log_prod.error(f"job= {self._id} | NO SE ENCONTRO LA CAJA MIS_COMP")
                    print('no se encontro la caja')
                    input_element = self.force_find_xpath(browser=self.browser, xpath="/html/body/div/div/main/div/section/div/div[2]/div/div[1]/div/div/div[1]/input", t_s=5)
                    input_element.send_keys('Mis Comprobantes')
                    time.sleep(1)
                    modal_element = self.force_find_xpath(browser=self.browser, 
                                                          xpath="/html/body/div/div/main/div/section/div/div[2]/div/div[1]/div/div/ul/li/a/div/div/div[2]/button", 
                                                          t_s=5, 
                                                          click=True,
                                                          name= 'Agregar')
                    log_prod.info(f"job= {self._id} | SE AGREGO CAJA NUEVA MIS_COMP Y SE ACCEDIO A ELLA ")
                    time.sleep(1)
                    time.sleep(t_s)

                    w_id = self.browser.current_window_handle

                    log_prod.info(f"job= {self._id} |w_id: {w_id}")

                    self.actual_window_2(self.browser, from_id=[w_id], n_windows_end=2, t_s=t_s)

                    return self    
                
              

        except (WebDriverException, AssertionError, Exception) as e:

            return self.return_exception(self.browser, self.data, e, close=False)

    def get_sales(self, t_s: float = None, headless: bool = True, t_o: float = None):
        log_prod.info(f"job= {self._id} |==========GETTING SALES===========")
        try:
            # SE CREA INSTANCIA EN LA BASE DE DATOS TASK.PY
            create_task(job_id=self._id,
                        servicio='ccma',
                        task_status="init-not-end",
                        task_error='not-error')
            
            self.queue.register("get_sales", self._id, self.cuit)

            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.mis_comprobantes.get_sales.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.mis_comprobantes.get_sales.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.mis_comprobantes.get_sales.headless", headless)

            run = self.run(t_s=t_s, headless=headless, t_o=t_o)

            if isinstance(run, dict):
                raise AssertionError(str(run.get("errors", "Unknow error")))

            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)

            XPATH_REPRESENTADO_NUEVO = "/html/body/form/main/div/div/div[2]/div/a/div/div[2]/p"

            time.sleep(2)

            representato = self.browser.find_elements_by_xpath(XPATH_REPRESENTADO_NUEVO)

            if len(representato) > 0:
                aux = representato[0].text.replace("-", "")

                if str(aux) == str(self.cuit):
                    representato[0].click()

            wait_ = WebDriverWait(self.browser, 60)
            error = "/html/body/main/div/section/div/div/div[2]"
            error = self.browser.find_elements_by_xpath(error)

            if len(error) > 0:
                patron = re.compile("ERR")

                if patron.search(error[0].text.upper()):
                    log_prod.error(f"job={self._id} FROM GET_SALES |  LA CUIT CONTIENEN IRREGULARIDADES ")
                    irregularidad_cuit = 'registra irregularidades'
                    if irregularidad_cuit in str(error[0].text):

                        # SE ACTUALIZA REGISTRO EN BASE DE DATOS TASK.PY COMO TAREA FALLIDA
                        update_task(job_id=self._id,
                                    task_status="failed",
                                    task_error=f" esta respuesta es get_sales mediania: {error[0].text}")

                        log_prod.warning(f'job={self._id} | FROM GET_SALES | RETORNANDO EXCEPCION CUIT IRREGULAR')
                       
                        self.logout()

                        return self.return_exception(self.browser, self.data, error[0].text)


                    response = msg.get_basic_message()
                    response = msg.update_message(response,
                                                  header={"fn": self.data["header"]["fn"]},
                                                  id=self.data["id"],
                                                  status=STATUS_OK,
                                                  payload={"ERROR": str(error[0].text)})
                    self.logout()

                    # estar pendiente de este error
                    # SE ACTUALIZA REGISTRO EN BASE DE DATOS TASK.PY COMO TAREA FALLIDA
                    update_task(job_id=self._id,
                                task_status="failed",
                                task_error=f" esta respuesta es get_sales mediania: {response}")

                    return response

            self.wait_and_go(xpath=XPATH_MISC_EMITIDOS, click=True)

            desde, hasta = self.data["payload"]["from"], self.data["payload"]["to"]

            #wait_.until(EC.element_to_be_clickable((By.XPATH, XPATH_MISC_BUSCAR)))

            self.wait_and_go(xpath=XPATH_MISC_RANGO_FECHA, click=False)

            fecha = self.force_find_xpath(self.browser, xpath=XPATH_MISC_RANGO_FECHA, click=False)

            fecha.clear()

            fecha.send_keys(desde+" - "+hasta+Keys.TAB)

            self.wait_and_go(xpath=XPATH_MISC_BUSCAR, click=True)

            # MANEJO DE ERROR CUANDO AL BUSCAR UN RECIBO AFIP TE REDIRIJE AL HISTORIAL

            time.sleep(random.uniform(1, 3))
            pestaña_ACTIVA = self.browser.find_element_by_xpath('//ul[@id="tabsComprobantes"]/li[@class="active"]').text

            if pestaña_ACTIVA == 'Historial':
                log_prod.error(f"job={self._id} | FROM MIS COMPROBANTES | LA PAGINA DIRIGE AL HISTORIAL NO A RECIBOS")
                result = 'NO SE PUDIERON DESCARGAR LOS RECIBOS. LA PAGINA DIRIGE AL HISTORIAL'

                # SE ACTUALIZA REGISTRO EN BASE DE DATOS TASK.PY COMO TAREA FALLIDA
                update_task(job_id=self._id, task_status="failed", task_error=result)

                raise ExceptionResultados(result)
            

            wait_.until(EC.element_to_be_clickable((By.XPATH, XPATH_MISC_DCSV)))

            XPATH_REPRESENTADO = "/html/body/header/nav/div/div/div[2]/div/span[2]/span"
            representado = self.browser.find_elements_by_xpath(XPATH_REPRESENTADO)

            cuit = self.cuit

            if len(representado) > 0:
                cuit = representado[0].text
                cuit = cuit[-14:].split("]")[0].replace("-", "")

            file_name = f"{NAME_BASE_MISC_EMITIDOS} {cuit}.csv"

            while not self.queue.next_service("get_sales", self.cuit) == self._id:
                log_prod.info(f"current job: {self._id}")
                time.sleep(1)

            self.wait_and_go(xpath=XPATH_MISC_DCSV, click=True)

            encoded = self.get_csv_64(file_name=file_name, d_p="/tmp")

            service = self.service.get(self.service.job_id == self._id)
            service.delete_instance()

            log_prod.info(f"job= {self._id} | ENDING PROCESS AND SENDING RESPONSE")

            response = msg.get_basic_message()
            response = msg.update_message(response,
                                          header={"fn": self.data["header"]["fn"]},
                                          id=self.data["id"],
                                          status=STATUS_OK,
                                          payload={"csv_ventas": str(encoded)})
            self.logout()

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

    def get_purchases(self, t_s: float = None, headless: bool = True, t_o: float = None):
        log_prod.info(f"job= {self._id} |==========GETTING PURCHASES===========")
        try:
            # SE CREA INSTANCIA EN LA BASE DE DATOS TASK.PY
            create_task(job_id=self._id,
                        servicio='ccma',
                        task_status="init-not-end",
                        task_error='not-error')

            self.queue.register("get_purchase", self._id, self.cuit)

            t_o = self.t_o if not t_o else t_o
            t_o = dpath(self.config, "scrapper.afip.mis_comprobantes.get_purchases.t_o", t_o)
            t_s = dpath(self.config, "scrapper.afip.mis_comprobantes.get_purchases.t_s", t_s)
            headless = dpath(self.config, "scrapper.afip.mis_comprobantes.get_purchases.headless", headless)

            run = self.run(t_s=t_s, headless=headless, t_o=t_o)

            if isinstance(run, dict):
                raise AssertionError(str(run.get("errors", "Unknow error")))

            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)

            XPATH_REPRESENTADO_NUEVO = "/html/body/form/main/div/div/div[2]/div/a/div/div[2]/p"

            time.sleep(2)

            representato = self.browser.find_elements_by_xpath(XPATH_REPRESENTADO_NUEVO)

            if len(representato) > 0:
                aux = representato[0].text.replace("-", "")

                if str(aux) == str(self.cuit):
                    representato[0].click()

            wait_ = WebDriverWait(self.browser, 60)

            error = "/html/body/main/div/section/div/div/div[2]"
            error = self.browser.find_elements_by_xpath(error)

            if len(error) > 0:
                patron = re.compile("ERR")

                if patron.search(error[0].text.upper()):

                    # MANEJO DE ERROR CUIT CON IRREGULARIDAD

                    irregularidad_cuit = 'registra irregularidades'
                    if irregularidad_cuit in str(error[0].text):
                        log_prod.error(f"job={self._id} | FROM GET_PURCHASES | LA CUIT CONTIENE IRREGULARIDADES ")

                        # SE ACTUALIZA REGISTRO EN BASE DE DATOS TASK.PY COMO TAREA FALLIDA
                        update_task(job_id=self._id,
                                    task_status="failed",
                                    task_error=f" esta respuesta es get_purchases mediania: {error[0].text}")


                        log_prod.warning(f'job={self._id} | FROM GET_PURCHASES | RETORNANDO EXCEPCION CUIT IRREGULAR')
                        return self.return_exception(self.browser, self.data, error[0].text)

                    
                    response = msg.get_basic_message()
                    response = msg.update_message(response,
                                                  header={"fn": self.data["header"]["fn"]},
                                                  id=self.data["id"],
                                                  status=STATUS_OK,
                                                  payload={"ERROR": str(error[0].text)})
                    self.logout()

                    # estar pendiente de este error
                    # SE ACTUALIZA REGISTRO EN BASE DE DATOS TASK.PY COMO TAREA FALLIDA
                    update_task(job_id=self._id,
                                task_status="failed",
                                task_error=f" esta respuesta es get_purchases mediania: {response}")
                    

                    return response

            self.wait_and_go(xpath=XPATH_MISC_RECIBIDOS, click=True)

            desde, hasta = self.data["payload"]["from"], self.data["payload"]["to"]

            wait_.until(EC.element_to_be_clickable((By.XPATH, XPATH_MISC_BUSCAR)))

            self.wait_and_go(xpath=XPATH_MISC_RANGO_FECHA, click=False)

            fecha = self.force_find_xpath(self.browser, xpath=XPATH_MISC_RANGO_FECHA, click=False)
            fecha.clear()
            fecha.send_keys(desde+" - "+hasta+Keys.TAB)

            self.wait_and_go(xpath=XPATH_MISC_BUSCAR, click=True)

            # MANEJO DE ERROR: CUANDO AL INGRESAR A LOS RECIBOS TE ENVIA AL HISTORIAL
            time.sleep(random.uniform(1, 3))
            pestaña_ACTIVA = self.browser.find_element_by_xpath('//ul[@id="tabsComprobantes"]/li[@class="active"]').text

            if pestaña_ACTIVA == 'Historial':
                log_prod.error(f"job={self._id} | FROM MIS COMPROBANTES | LA PAGINA DIRIGE AL HISTORIAL NO A RECIBOS")
                result = 'NO SE PUDIERON DESCARGAR LOS RECIBOS. LA PAGINA DIRIGE AL HISTORIAL'

                # SE ACTUALIZA REGISTRO EN BASE DE DATOS TASK.PY COMO TAREA FALLIDA
                update_task(job_id=self._id, task_status="failed", task_error=result)

                raise ExceptionResultados(result)


            wait_.until(EC.element_to_be_clickable((By.XPATH, XPATH_MISC_DCSV)))

            XPATH_REPRESENTADO = "/html/body/header/nav/div/div/div[2]/div/span[2]/span"
            representado = self.browser.find_elements_by_xpath(XPATH_REPRESENTADO)
            cuit = self.cuit

            if len(representado) > 0:
                cuit = representado[0].text
                cuit = cuit[-14:].split("]")[0].replace("-", "")

            file_name = f"{NAME_BASE_MISC_RECIBIDOS} {cuit}.csv"

            while not self.queue.next_service("get_purchase", self.cuit) == self._id:
                log_prod.info(f"current job: {self._id}")
                time.sleep(1)

            time.sleep(random.choice([1, 2, 3]))

            self.wait_and_go(xpath=XPATH_MISC_DCSV, click=True)

            encoded = self.get_csv_64(file_name=file_name, d_p="/tmp")

            service = self.service.get(self.service.job_id == self._id)
            service.delete_instance()

            log_prod.info(f"job= {self._id} | ENDING PROCESS AND SENDING RESPONSE")

            response = msg.get_basic_message()
            response = msg.update_message(response,
                                          header={"fn": self.data["header"]["fn"]},
                                          id=self.data["id"],
                                          status=STATUS_OK,
                                          payload={"csv_ventas": str(encoded)})
            self.logout()

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
    import uuid
    import threading

    def hilo(message):
        print(message)
        result1 = MisComprobantes(**message).get_purchases()
        result2 = MisComprobantes(**message).get_sales()
        print(result1)
        print(result2)

    cuit = 1
    pwd = "a"
    ventas1 = {
        "message": {
            "status": 0,
            "errors": [],
            "id": str(uuid.uuid4()),
            "header": {
                "auth": {
                    "codif": 0,
                    "cuit": cuit,
                    "password": pwd,
                    "type": "basic"
                },
                "job_service": "afip",
                "fn": "anfler_afip.anfler_mis_comprobantes.MisComprobantes@get_sales",
                "key": None,
                "offset": 0,
                "partition": 0
            },
            "payload": {
                "to": "30-01-2023",
                "from": "01-01-2023"
            },
        }
    }
    ventas2 = {
        'message': {
            'status': 0,
            'errors': [],
            'id': str(uuid.uuid4()),
            'header': {
                'auth': {
                    'codif': 0,
                    'cuit': cuit,
                    'password': pwd,
                    'type': 'basic'
                },
                'job_service': "afip",
                'fn': 'anfler_afip.anfler_mis_comprobantes.MisComprobantes@get_sales',
                'key': None,
                'offset': 0,
                'partition': 0
            },
            'payload': {
                'from': '01-02-2020',
                'to': '30-02-2020',
            },
        }
    }
    ventas3 = {
        'message': {
            'status': 0,
            'errors': [],
            'id': str(uuid.uuid4()),
            'header': {
                'auth': {
                    'codif': 0,
                    'cuit': cuit,
                    'password': pwd,
                    'type': 'basic'
                },
                'job_service': "afip",
                'fn': 'anfler_afip.anfler_mis_comprobantes.MisComprobantes@get_sales',
                'key': None,
                'offset': 0,
                'partition': 0
            },
            'payload': {
                'from': '01-03-2020',
                'to': '30-03-2020',
            },
        }
    }
    ventas4 = {
        'message': {
            'status': 0,
            'errors': [],
            'id': str(uuid.uuid4()),
            'header': {
                'auth': {
                    'codif': 0,
                    'cuit': cuit,
                    'password': pwd,
                    'type': 'basic'
                },
                'job_service': "afip",
                'fn': 'anfler_afip.anfler_mis_comprobantes.MisComprobantes@get_sales',
                'key': None,
                'offset': 0,
                'partition': 0
            },
            'payload': {
                'from': '01-04-2020',
                'to': '30-04-2020',
            },
        }
    }
    ventas5 = {
        'message': {
            'status': 0,
            'errors': [],
            'id': str(uuid.uuid4()),
            'header': {
                'auth': {
                    'codif': 0,
                    'cuit': cuit,
                    'password': pwd,
                    'type': 'basic'
                },
                'job_service': "afip",
                'fn': 'anfler_afip.anfler_mis_comprobantes.MisComprobantes@get_sales',
                'key': None,
                'offset': 0,
                'partition': 0
            },
            'payload': {
                'from': '01-05-2020',
                'to': '30-05-2020',
            },
        }
    }
    ventas6 = {
        'message': {
            'status': 0,
            'errors': [],
            'id': str(uuid.uuid4()),
            'header': {
                'auth': {
                    'codif': 0,
                    'cuit': cuit,
                    'password': pwd,
                    'type': 'basic'
                },
                'job_service': "afip",
                'fn': 'anfler_afip.anfler_mis_comprobantes.MisComprobantes@get_sales',
                'key': None,
                'offset': 0,
                'partition': 0
            },
            'payload': {
                'from': '01-06-2020',
                'to': '30-06-2020',
            },
        }
    }

    thread1 = threading.Thread(target=hilo, args=(ventas1, ))
    #thread2 = threading.Thread(target=hilo, args=(ventas2, ))
    #thread3 = threading.Thread(target=hilo, args=(ventas3, ))
    #thread4 = threading.Thread(target=hilo, args=(ventas4, ))
    #thread5 = threading.Thread(target=hilo, args=(ventas5, ))
    #thread6 = threading.Thread(target=hilo, args=(ventas6, ))
    thread1.start()
    #thread2.start()
    #thread3.start()
    #thread4.start()
    #thread5.start()
    #thread6.start()
    thread1.join()
    #thread2.join()
    #thread3.join()
    #thread4.join()
    #thread5.join()
    #thread6.join()

