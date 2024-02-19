from anfler_base.anfler_baseclass import BaseClass, log_prod, log_dev
from anfler_base.decorators import random_wait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from anfler_agip.settings import *
from anfler.util.helper import dpath
from os.path import join, exists
from os import mkdir
import time


class Login(BaseClass):

    def __init__(self, cuit: int, pwd: str, browser="chrome", t_s: float = 0.2,
                 t_o: float = 60, id_: str = None, change_dir=False):
        """
        :param cuit: int CUIT of taxpayer
        :param pwd: str contraseña of taxpayer
        """
        super(Login, self).__init__(browser=browser, id_=id_)  # por default la BaseClass corre chrome
        self.cuit, self.pwd = self.validate(cuit, pwd)
        self.url = URL_LOGIN_AGIP
        self.t_s = dpath(self.config, "scrapper.t_s", t_s)
        self.t_o = dpath(self.config, "scrapper.t_o", t_o)
        self._change_dir = change_dir

    def change_dir(self, opciones: dict):
        new_dir = join(DOWNLOADS_PATH, self._id)
        if not exists(new_dir):
            mkdir(new_dir)
        opciones["download.default_directory"] = new_dir
        return opciones

    @random_wait()
    def run(self, xpath: tuple = C_XPATH_LOGIN_AGIP, t_s=None, t_o=None, options=True, headless=False) -> webdriver:
        """
        :xpath: tuple of two strings ('str', 'str') where index 0 its related to username and index 1 to password
        :t_s: float it's time sleep between all the steps of the workflow
        """
        log_prod.info(f"job= {self._id}| LOGGING AT URL: {self.url}")
        log_prod.info(f"job= {self._id}| SETTING OPTIONS OF DRIVER")
        t_o = self.t_o if not t_o else t_o
        t_s = self.t_s if not t_s else t_s
        try:
            assert (self.browser in DRIVERS_ALLOWED.keys()), \
                log_prod.error(f"job= {self._id}| browser is not in settings.DRIVERS_ALLOWED")
            if self.browser == "chrome":
                log_prod.info(f"job= {self._id}| ====================DRIVER SELECTED: CHROME====================")
                if options:
                    opciones = webdriver.ChromeOptions()
                    opciones.arguments[:] = []
                    opciones.add_argument("--incognito")
                    opciones.add_argument("--crash-on-failure")
                    opciones.add_argument("--no-sandbox")
                    if headless:
                        opciones.add_argument("--headless")
                    opciones.add_argument('--disable-dev-shm-usage')
                    if self._change_dir:
                        OPTIONS_DRIVER["chrome"]["options"] = self.change_dir(OPTIONS_DRIVER["chrome"]["options"])
                    print()
                    opciones.add_experimental_option("prefs", OPTIONS_DRIVER["chrome"]["options"])
                    options = opciones
                self.browser = webdriver.Chrome(executable_path=OPTIONS_DRIVER["chrome"]["path"], options=options)
            elif self.browser == "firefox":
                log_prod.info(f"job= {self._id}| ====================DRIVER SELECTED: FIREFOX====================")
                if options:
                    from selenium.webdriver.firefox.options import Options
                    opciones = Options()
                    # opciones.add_argument("--incognito")
                    if headless:
                        opciones.add_argument("--headless")
                    # opciones.set_preference("browser.download.dir", d_p)
                    opciones.set_preference("browser.download.dir", DOWNLOADS_PATH)
                    opciones.set_preference("browser.download.folderList", 2)
                    opciones.set_preference("browser.download.manager.showWhenStarting", False)
                    opciones.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
                    options = opciones
                if t_s < 2:
                    t_s = 2
                self.browser = webdriver.Firefox(executable_path=OPTIONS_DRIVER["firefox"]["path"], options=options)
            self.browser.set_page_load_timeout(t_o)
            self.browser.get(self.url)
            self.get_status_200(self.browser)
            cuit = self.wait_and_go(xpath=xpath[0], click=False)
            pwd_ = self.wait_and_go(xpath=xpath[1], click=False)
            cuit.send_keys(str(self.cuit))
            pwd_.send_keys(f"{self.pwd}" + Keys.RETURN)
            self.browser.maximize_window()
            log_prod.info(f"job= {self._id} |LOGGED continue")
            return self.browser
        except (WebDriverException, Exception) as e:
            log_prod.error(f"job= {self._id}|{str(e)}")
            status_page = self.get_status(self.browser)
            self.logout()
            return status_page + str(e)


if __name__ == "__main__":
    from factory.usuarios import u_agip
    l = Login(cuit=u_agip['cuit'], pwd=u_agip['password'])
    a = l.run(headless=False)