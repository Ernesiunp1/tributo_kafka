from anfler_base.anfler_baseclass import log_prod
from anfler.util.helper import dpath
import anfler.util.config.cfg as cfg
from functools import wraps
import random
import time

cfg.load(["/app/anfler-webscrap/etc/config_afip.json"], ignore_errors=True)
decorar = dpath(cfg.config, "scrapper.decorar", True)
min_time_random = dpath(cfg.config, "scrapper.time_random_min", 2)
max_time_random = dpath(cfg.config, "scrapper.time_random_max", 8)


def validate_pwd(f):
    def wrap(*args, **kwargs):
        print("algo")
        return f(*args, **kwargs)
    return wrap


def random_wait(min_time: int = 8, max_time: int = 10):
    def intern(f):
        @wraps(f)
        def wrap(*arg, **kwargs):
            if decorar:
                # t = random.randint(min_time, max_time)
                t = random.uniform(min_time_random, max_time_random)
                log_prod.warning(f"==================DECORADOR RANDOM_WAIT EN USO t_s = {t}====================")
                kwargs["t_s"] = t
                return f(*arg, **kwargs)
            else:
                return f(*arg, **kwargs)
        return wrap
    return intern
