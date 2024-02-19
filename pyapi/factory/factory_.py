import random

from servicios_varios import *
import importlib
from json import dumps
from pprint import pprint


def factory2(cls, *args, **kwargs):
    metod = kwargs["metodo"]
    del kwargs["metodo"]
    obj = getattr(cls(*args, **kwargs), metod)
    return obj


def wrap_message(message, key_0="message", key_1="header", key_2="fn", sep="@"):
    # ej. 'anfler_afip.ccma.CCMA@run' que estructuralmente seria paquete.modulo/s@metodo
    mensaje = message[key_0][key_1][key_2]
    split = mensaje.split(sep)
    pkg, met = split[0], split[1]
    split = pkg.split(".")
    organismo = split[0]  # 'anfler_afip'
    paquete = split[1]  # 'anfler_constancia_inscripcion'
    clase = split[2]  # split[2] = 'Constancia'
    funcion = met  # 'get_address'
    return organismo, paquete, clase, funcion


def _get_class_method(msj):
        org, p, c, m = wrap_message(msj)
        aux = org + "." + p
        return aux, c, m


def execute_class_method(string_func, init_args=None, args=None):
    """Execute dynamically the method defined in string_func. See _get_class_method() for valid format

    :param string_func: Class@method to be executed
    :param init_args: Class params (_init_)
    :param args: Method params
    :return: Output of execution
    """
    if not string_func or len(string_func) == 0:
        raise ValueError(f"Invalid value '{string_func}', argument must be '<full package name>.<ClassName>@<method>'")
    package_, class_, method_ = _get_class_method(string_func)
    # print(package_, class_, method_)
    if not class_:
        raise ValueError(f"Invalid value '{string_func}', argument must be '<full package name>.<ClassName>@<method>'")
    res = None
    klass = importlib.import_module(package_)
    obj_ = getattr(klass, class_)(**init_args)
    func_ = getattr(obj_, method_)
    return func_


if __name__ == '__main__':
    # suponiendo que el mensaje trae como funcion la descripcion completa
    # ej. 'anfler_afip.ccma.CCMA@run' que estructuralmente seria paquete.modulo/s@metodo
    servicios = [direccion, ventas2, captura, ccma, categoria, actividad]
    servicio = random.choice(servicios)
    servicio = captura
    org, paq, cls, fun = wrap_message(servicio)
    modulo = importlib.import_module(f"{org}.{paq}")
    clase = getattr(modulo, cls)
    p = execute_class_method(servicio, servicio)
    payload = p()
    payload = dumps(payload, ensure_ascii=False)
    pprint(payload)
