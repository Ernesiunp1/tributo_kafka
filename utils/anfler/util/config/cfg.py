"""Helper to handle configuration files (json format)
"""

import json
import os

config_files = set()
config=None



def __load_json_file(filename):
    _config={}
    with open(filename) as json_file:
        _config = json.load(json_file)
    return _config

def __replace_item(obj, key, replace_value):
    """
    Replaces the dictionary value of key with replace_value in the obj dictionary.
    """
    if key in obj:
        obj[key] = replace_value

    for k, v in obj.items():
        if isinstance(v, dict):
            __replace_item(v, key, replace_value)

def load(files,ignore_errors=False):
    """Load configuration file (JSON format)

    Args:
        files: List of JSON files (path and name)
        ignore_errors: Ignore any error and continue
    """
    global config , config_files
    _files=[]
    if isinstance(files, str):
        _files=[files]
    else:
        _files = files

    try:
        for f in _files:
            file=os.path.basename(f.strip())
            if file in config_files:
                continue
            else:
                if config == None:
                    config = {}
                config.update(__load_json_file(f))
                # with open(f) as json_file:
                #     _config  = json.load(json_file)
                #     config.update(_config)
                config_files.add(file)
    except Exception as e:
        if ignore_errors:
            pass
        else:
            raise e


def load_from_env(env_vars,ignore_errors=True):
    """Load configuration  (JSON format) from environments variables

    Args:
        env_vars: List of environment variables containing JSON configuration
        ignore_errors: Ignore any error and continue
    """
    global config , config_files
    vars_=[]
    if isinstance(env_vars, str):
        vars_=[env_vars]
    else:
        vars_ = env_vars
    for v in vars_:
        try:
            json_=os.environ[v]
            if config == None:
                config = {}
            config.update(json.loads(json_))
            config_files.add(v)
        except Exception as e:
            if ignore_errors:
                pass
            else:
                raise e

def get(key,default=None, return_default=False):
    """Get value for key

    Args:
        :param key: key name, inner keys in format 'key1.key2'
        :default: Default value to return if key doesn't exist (only if return_default==True)
        :return_default: Return default value
    Returns:
        key value or KeyError if not found
    """
    global  config
    if config == None:
        raise Exception(f"Non configuration loaded, execute load() to load it")
    items = key.split(".")
    # print(items)
    obj = config
    try:
        for k in items:
            obj = obj[k]
    except KeyError:
        if return_default :
            return default
        else:
            raise NameError(f"Key {key} not found")
    return obj
