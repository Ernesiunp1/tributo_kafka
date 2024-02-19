from anfler_afip.anfler_ccma import CCMA
from anfler_afip.anfler_constancia_inscripcion import Constancia
from ejemplo_kaftka import mensaje_kafka, msg_kafka_json, from_kafka
from anfler_afip.anfler_comprobantes import Comprobantes
from anfler_afip.anfler_mis_comprobantes import MisComprobantes
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import base64
import time
# import anfler.util.log.lw as lw
import etc.logging.logging_wrapper as lw
import pprint


def ver_imgen_base_64(image_64, title):
    # _log_prod.info("OPENING IMAGE AND PLOTTING")
    im = Image.open(BytesIO(base64.b64decode(image_64)))
    plt.imshow(im)
    plt.title(title)
    plt.show()


def afip_ccma(message, t_s=1, headless=True, *args, **kwargs):
    # _log_prod.info("SEARCH FOR CCMA")
    response = CCMA(message, t_s=t_s).run(t_s=t_s, headless=headless)
    # print(response)
    return response


def get_registration_proof(message, t_s=1, headless=True, *args, **kwargs):
    # _log_prod.info("SEARCH FOR CONSTANCIA IMAGE")
    response = Constancia(message, t_s=t_s).get_image(headless=headless)
    #aux = eval(response)
    # ver_imgen_base_64(aux["data_out"]["image"], title="F183")
    return response


def get_activity(message, t_s=1, headless=True, *args, **kwargs):
    # _log_prod.info("SEARCH FOR ACTIVITY")
    response = Constancia(message, t_s=t_s).get_activity(t_s=t_s, headless=headless)
    return response


def get_address(message, t_s=1, headless=True, *args, **kwargs):
    # _log_prod.info("SEARCH FOR ADDRESS")
    response = Constancia(message, t_s=t_s).get_address(t_s=t_s, headless=headless)
    return response


def see_sales(message, t_s=1, headless=True, *args, **kwargs):
    comp = Comprobantes(message, t_s=t_s).get_sales(t_s=t_s, headless=headless, t_o=60)
    return comp


def see_purchases(message, t_s=1, headless=True, *args, **kwargs):
    comp = Comprobantes(message, t_s=t_s).get_purchases(t_s=t_s, headless=headless, t_o=10)
    return comp


def see_category(message, t_s=1, headless=True, *args, **kwargs):
    cat = Constancia(message, t_s=t_s).get_category(t_s=t_s, headless=headless, t_o=5)
    return cat


def see_my_sales(message, t_s=1, t_o=20, headless=True, *args, **kwargs):
    aux = MisComprobantes(message, t_s=t_s).get_sales(t_s=t_s, headless=headless, t_o=t_o)
    return aux


if __name__ == "__main__":
    lw.init_logging("../factory/logging_test.json")
    for x in range(1):
        #pprint.pprint(see_category(**from_kafka))  # pass
        #time.sleep(t)
        #pprint.pprint(get_address(**from_kafka))  # pass
        #time.sleep(t)
        #print(afip_ccma(**from_kafka, headless=True))  # pass
        #time.sleep(t)
        #print(get_registration_proof(**from_kafka))  # pass
        #time.sleep(t)
        #pprint.pprint(get_activity(**from_kafka))  # pass
        #time.sleep(t)
        #pprint.pprint(see_sales(**from_kafka))
        #time.sleep(t)
        #### see_purchases(mensaje_kafka) # Notimplemented
        #time.sleep(t)
        pprint.pprint(see_my_sales(**from_kafka, headless=True))  # pass
