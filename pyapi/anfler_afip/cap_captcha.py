import os.path
import urllib.request
import cv2
import pytesseract
import numpy as np
from selenium.webdriver.common.keys import Keys
from anfler_base.anfler_baseclass import BaseClass, log_prod, log_dev
from selenium.webdriver.common.by import By
#from .update_Vpn import contador_captcha
import time
import re

texto_esperado = ""
mensaje_devuelto = ""
contador1 = 0


def captchas_try(self):
    log_prod.warn(f"job= {self._id}|  INICIALIZANDO CAP_CAPTCHA ")
    global contador1
    # Buscando imagen por al alt
    try:
        time.sleep(1)
        xpath_pwd_captcha = '/html/body/main/div/div/div/div/div/div/form/div/input[2]'
        input_pwd = self.browser.find_element(By.XPATH, xpath_pwd_captcha)
        time.sleep(2)

        input_xpath1 = '//*[@id="F1:captchaSolutionInput"]'
        input_element1 = self.browser.find_element(By.XPATH, input_xpath1)

        boton = self.browser.find_element_by_css_selector("#F1\\:btnIngresar")

        if xpath_pwd_captcha and input_xpath1 and boton:
            time.sleep(2)
            imagen_url = self.browser.find_element_by_xpath(
                "/html/body/main/div/div/div/div/div/div/form/div/div[2]/img").get_attribute('src')
            #contador_captcha()

            # Configurando directorios de destino para descargas
            # dir_captcha = "afip_captcha"
            # dir_captcha_pros = "afip_captcha_procesado"
            dir_captcha = "/app/logs/afip_captcha"
            dir_captcha_pros = "/app/logs/afip_captcha_procesado"

            if not os.path.exists(dir_captcha):
                os.mkdir(dir_captcha)
                log_prod.info(f"job= {self._id} | Se creo el directorio dir_captcha ")
            else:
                log_prod.info('la carpeta dir_captcha ya existe')

            # Path donde se guaradara la imagen fuera de pyapi
            path_destino = dir_captcha


            # Calculando la cantidad de imagenes en el directorio para asignarle nombre a la imagen
            archivos = os.listdir(path_destino)
            cant_archivos = len(archivos)
            # print('cantidad de archivos: ', cant_archivos)

            # Guardando la imagen en la ruta de destino
            urllib.request.urlretrieve(imagen_url, path_destino + "/" +str(cant_archivos) + ".png")
            image = cv2.imread( path_destino + "/" + str(cant_archivos) + ".png")
            # cv2.imshow('prueba de imagen', image)
            # cv2.waitKey(1000)

            # image = cv2.imread('imagen.png')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Aplicar umbralización
            _, thresh = cv2.threshold(gray, 0, 250, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # Aplicar erosión y dilatación
            kernel = np.ones((0, 7), np.uint8)
            erosion = cv2.erode(thresh, kernel, iterations=1)
            dilation = cv2.dilate(erosion, kernel, iterations=0)

            image = cv2.bitwise_not(dilation)

            # Guardar la imagen procesada
            if not os.path.exists(dir_captcha_pros):
                os.mkdir(dir_captcha_pros)
                log_prod.warn( f"job= {self._id} | Se creo el directorio dir_captcha_pros")
            else:
                log_prod.info( f"job= {self._id} | El directorio dir_captcha_pros ya existe")

            path_destino_2 = dir_captcha_pros

            cv2.imwrite( path_destino_2 + "/" + str(cant_archivos) + "processed.png", image)
            print('imagen guaradada')

            # Segundo procesamiento
            image = cv2.imread( path_destino_2 + "/" + str(cant_archivos) + "processed.png")
            # cv2.imshow('prueba de imagen', image)
            # cv2.waitKey(1000)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Aplicar umbralización
            _, thresh = cv2.threshold(gray, 0, 250, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # Aplicar erosión y dilatación
            kernel = np.ones((1, 5), np.uint8)
            erosion = cv2.erode(thresh, kernel, iterations=0)
            dilation = cv2.dilate(erosion, kernel, iterations=0)
            image = cv2.bitwise_not(dilation)

            # Guardar la imagen procesada
            cv2.imwrite(path_destino_2 + "/" + str(cant_archivos) + "processed2.png", image)
            text = pytesseract.image_to_string(image)
            # print('Texto: ', text)

            # Manejo string text
            text = text.strip()
            text = text.replace(" ", "")
            text = re.sub('[^a-zA-Z0-9]', '', text)
            text = re.sub(r'[^\w\s]', '', text)
            if len(text) > 6:
                text = text.lstrip(text[0])
            #print('Texto: ', text)

            # Enviando el Captcha al input:
            self.browser.maximize_window()
            # print('voy por xpath')
            input_xpath1 = '//*[@id="F1:captchaSolutionInput"]'
            input_element1 = self.browser.find_element(By.XPATH, input_xpath1)
            input_element1.click()
            time.sleep(1)
            input_element1.send_keys(text)
            time.sleep(1)

            # Enviando la clave al input en la pantalla de captcha:
            xpath_pwd_captcha = '/html/body/main/div/div/div/div/div/div/form/div/input[2]'
            input_pwd = self.browser.find_element(By.XPATH, xpath_pwd_captcha)
            input_pwd.click()
            time.sleep(1)
            input_pwd.send_keys(f"{self.pwd}")
            time.sleep(1)

            # Ubicando boton Ingresar y presionando Enter
            boton = self.browser.find_element_by_css_selector("#F1\\:btnIngresar")
            boton.send_keys(Keys.ENTER)
            time.sleep(5)

            # Buscando y extrayendo el texto del alert
            selector = self.browser.find_element_by_css_selector("#F1\:msg")

            # evaluando el texto para saber si se ejecuta el while o no
            if selector:
                #print(selector.text)
                mensaje_devuelto = selector.text
                texto_esperado = "El captcha ingresado es incorrecto."
                texto_esperado2 = 'Clave o usuario incorrecto'

                # if texto alert == captcha invalido
                if mensaje_devuelto == texto_esperado:
                    while contador1 < 2:
                        contador1 += 1
                        # print('contador: ', contador1)
                        captchas_try(self)
                        log_prod.error(f"job= {self._id}|CAPTCHA INVALIDO")
                        resp_cap_invalido = f'job= {self._id}|CAPTCHA INVALIDO'
                        return resp_cap_invalido

                        # return False

                # if texto alert continua siendo captcha invalido hace ultimo intento
                elif mensaje_devuelto == texto_esperado:
                    # print('capcha invalido')
                    log_prod.error(f"job= {self._id}|CAPTCHA INVALIDO")
                    resp_cap_invalido = f'job= {self._id}|CAPTCHA INVALIDO'
                    return resp_cap_invalido
                    # return False

                # if texto alert es clave incorrecta:
                elif mensaje_devuelto == texto_esperado2:
                    # print('La clave es incorrecta')
                    log_prod.error(f"job= {self._id}|CLAVE INVALIDA FROM CAP_CAPTCHA")
                    resp_pwd_invalida = f"job= {self._id}|CLAVE INVALIDA FROM CAP_CAPTCHA"
                    return resp_pwd_invalida

                # if texto alert es diferente a clave incorrecta y al mismo tiempo es diferente a captcha incorrecto
                elif mensaje_devuelto != texto_esperado and mensaje_devuelto != texto_esperado2:
                    log_prod.info(f"job= {self._id}|  FROM CAP_CAPTCHA CAPTCHA RESUELTO")

                    XPATH_TODOS = "/html/body/div/div/main/section[1]/div/div/div/div[5]/div/a"
                    time.sleep(2)

                    self.wait_and_go(xpath=XPATH_TODOS, click=True)
                    # todos = self.browser.find_elements_by_xpath(XPATH_TODOS)
                    # if len(todos) > 0: todos[0].click()
                    log_prod.info(f"job= {self._id}|LOGGED continue")
                    return self.browser

                    #return True

    except:
        return None