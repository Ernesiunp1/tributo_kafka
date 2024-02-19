"""Wrapper function to execute Class.method"""
import importlib
import sys
import anfler.util.config.cfg as cfg
import anfler.util.log.lw as lw

_log= lw.get_logger("anfler.mp.helper")

#---------------------------------------------------------------------------
#   Import modules
#---------------------------------------------------------------------------
def import_modules(modules=[]):
    """
    :param modules:
    :return:
    """
    if len(modules) == 0:
        _log.warning(f"Modules list empty")
        return
    for m in modules:
        try:
            #__import__(m)
            importlib.import_module(m)
            _log.info(f"Module {m} imported")
        except ModuleNotFoundError as mnf:
            _log.warning(f"Module '{m}' not found. ({str(mnf)})")
        except Exception as e:
            _log.warning(f"Error loading module {m}. (str(e)")


def _get_class_method(string_func):
    """Extract package, class and function name from string_func

    :param string_func:  Expected format
       <full package>.<class name>@<class_method>
       or
       <method>

    :return: list containing (package, class_name , method) or (None,None, string_func)
    if it doesn't belong to a class
    """
    values = string_func.split("@", 1)
    package_= None
    class_ = None
    method_ = None

    if len(values) == 2:
        method_ = values[1]
        values2 =values[0].split(".")
        if len(values2) >= 2:
            if (values2[-1])[0].isupper():
                class_ = values2[-1]
                package_ = ".".join(values2[:-1])
            else:
                package_=values[0]
    else:
        method_ = string_func
    return (package_,class_,method_)

def execute_class_method(string_func, init_args=None,method_args=None):
    """Execute dynamically the method defined in string_func. See _get_class_method() for valid format

    :param string_func: Class@method to be executed
    :param init_args: Class params (__init__)
    :param args: Method params
    :return: Output of execution
    """
    if string_func == None or len(string_func) == 0:
        raise ValueError(f"Invalid value '{string_func}', argument must be '<full package name>.<ClassName>@<method>'")
    package_,class_, method_= _get_class_method(string_func)
    if class_ == None:
        raise ValueError(f"Invalid value '{string_func}', argument must be '<full package name>.<ClassName>@<method>'")
    #_log.debug(f"Executing package={package_} class={class_} init_args={init_args} method={method_} method_args={method_args}")
    res = None
    module_ = importlib.import_module(package_)
    klass_ = getattr(module_,class_)
    obj_ = klass_(**init_args)
    func_ = getattr(obj_,method_)
    return func_(**method_args)



