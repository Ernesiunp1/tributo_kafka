from anfler_base.anfler_baseclass import BaseClass, log_prod
from anfler_afip.settings import *
from anfler_afip.anfler_login import Login
from selenium.common.exceptions import *
from anfler.util.msg import message as msg
from anfler.util.helper import dpath


class Validate(BaseClass):

    def __init__(self, message: (dict, str), browser="chrome", t_s: float = 0.5,
                 options: bool = True, *args, **kwargs):
        super(Validate, self).__init__(browser=browser)
        log_prod.info("INSTANCING CONSTANCIA CLASS")
        self.data = self.validate_message(message)
        cuit, pwd = self.extract_cuit_pwd(self.data)
        self.cuit, self.pwd = self.validate(cuit, pwd)
        self._id = self.data["id"]
        self.browser = dpath(self.config, "scrapper.afip.validate_pwd.browser", browser)
        self.t_s = dpath(self.config, "scrapper.afip.validate_pwd.t_s", t_s)
        self.options = dpath(self.config, "scrapper.afip.validate_pwd.options", options)
        self.headless = dpath(self.config, "scrapper.afip.validate_pwd.headless", True)

    def run(self, t_s: float = 1, t_o: float = None, headless: bool = None):
        log_prod.info(f"job= {self._id}|START BROWSER TO CERTIFICATE")
        headless = self.headless if not headless else headless
        try:
            self.browser = Login(self.cuit,
                                 self.pwd,
                                 browser=self.browser,
                                 t_o=t_o, id_=self._id).run(C_XPATHS_LOGIN,
                                              t_s=t_s,
                                              options=self.options,
                                              headless=headless)
            if not self.validate_browser(self.browser):
                raise SessionNotCreatedException(self.browser)
            response = msg.get_basic_message(header={"fn": self.data["header"]["fn"]}, payload={"USER/PASSWORD": "OK"})
            response = msg.update_message(response, id=self.data["id"], status=STATUS_OK)
            self.logout()
            return response
        except (WebDriverException, Exception) as e:
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
                    'cuit': 20000000,
                    'password': "xxxxxxx",
                    'type': 'basic'
                },
                'job_service': "afip",
                'fn': 'anfler_afip.anfler_validate_password.Validate@run',
                'offset': 0,
                'partition': 0
            },
            'payload': {},
        }
    }
    a = Validate(**ccma).run()
    print(a)