"""Helpers
"""
import copy

import psutil
import os
import signal


# ---------------------------------------------------------------------------
#   Mask data
# ---------------------------------------------------------------------------
MASK_ITEMS=[
    "header.auth.password"
]
def mask_data(d, overwrite=False):
    """Mask data from dict using MASK_ITEMS

    :param d: dict
    :param overwrite: overwrite dict or not
    :return: dict masked
    """
    _d = d
    if overwrite == False:
        _d = copy.deepcopy(d)
    o=_d
    try:
        for m in MASK_ITEMS:
            elems=m.split(".")
            for e in elems[:-1]:
                o=o.get(e)
            o[elems[-1]] ="XXXXXX"
    except:
        pass
    return _d
# ---------------------------------------------------------------------------
#   Extract element from dict
# ---------------------------------------------------------------------------
def dpath(d, path=".", default=None):
    """Dot path function to traverse dictionary using "."
    :param d: dictionary
    :param path: keys path, e.g: "key1.key2.key3"
    :param default: None
    :return: Dictionary value for key d.get("key1").key("key2").get("key3") or default
    """
    if path == None:
        if d == None:
            return default
        else:
            return d
    if path == ".":
        return d
    # remove leading .
    if path.startswith("."):
        path = path[1:]

    items = path.split(".")
    obj = d

    try:
        for i in items:
            obj = obj.get(i)
            # print("\t" +str(obj))
    except AttributeError:
        obj = None
    if default != None and obj == None:
        return default
    return obj




# ---------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------
def get_childs_process_details(proces_names=[]):
    childs = get_childs_process(proces_names)
    # num_childs = len(childs)
    # num_childs_thds = sum([len(c.threads()) for c in childs])
    # _log.warning(f"Timeout task: Active childs={num_childs} num_child_thds={num_childs_thds}")
    process_info={}
    for i, child in enumerate(childs):
        try:
            thds = [t.id for t in child.threads()]
            process_info[child.pid] = {"pid": child.pid,
                                       "ppid": child.ppid(),
                                       "name": child.name(),
                                       "thds_num": len(thds),
                                       "thds": thds,
                                       "create_time": child.create_time(),
                                       "status": child.status()}
        except:
            pass
        #_log.warning(f"Timeout task: #{i:02d} pid={child.pid} name={child.name()} num_threads={len(thds)} threads={[t.id for t in thds]}")
        #_log.warning(f"Timeout task: Active childs={num_childs} num_child_thds={num_childs_thds}")
    return process_info
# ---------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------
def get_childs_process(proces_names=[]):
    """Return a lit of child processes (https://psutil.readthedocs.io/en/latest/#psutil.Process) ordered according to process_names

    Args:
        proces_names: List of process name to filter

    Returns:
        List of child processes
    """
    childs =[]
    try:
        current_process = psutil.Process()
        childs_ = current_process.children(recursive=True)
        if len(proces_names) > 0:
            for p in proces_names:
                childs += list(filter(lambda x: x.name() == p,childs_))
            #childs = list(filter(lambda x: x.name() in proces_names, childs_))
        else:
            childs = childs_
    except Exception as e:
        pass
    return childs


def kill_process(pid):
    os.kill(pid, signal.SIGTERM)
    os.kill(pid, signal.SIGKILL)