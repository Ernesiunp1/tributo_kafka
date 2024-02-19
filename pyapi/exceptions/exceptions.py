
def validate(cuit: int, pwd: str) -> tuple:
    """
    Validation of type cuit and pwd
    :return: cuit, pwd if this have the correct type, else raise TypeError
    """
    if cuit and pwd:
        if isinstance(cuit, int) and isinstance(pwd, str):
            return cuit, pwd
        else:
            raise Exception(TypeError, f"CUIT and pwd must be <class 'int'> and <class 'str'> "
                                       f"but are {type(cuit)} and {type(pwd)}")



class ExceptionResultados(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
