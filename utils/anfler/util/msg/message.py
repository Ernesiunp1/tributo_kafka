"""BASIC_MESSAGE struct and functions
"""

import copy
import uuid
from anfler.util.helper import dpath
import anfler.util.constants as C

"""Wrapper for each message"""
_BASIC_MESSAGE={
    "id": None,
    "header":{ "key": None,
               "service":C.DEFAULT_EMPTY,
               "fn": "full.package.Class@method",
               "entity":"",
               "user":C.DEFAULT_EMPTY ,
               "auth":{ "type":"basic"}},
    "payload": {},
    "status": 0,
    "errors": []
}


def simple_message(mensaje_de_error):

    nuevo_mensaje = str(mensaje_de_error)
    if "Password invalid" in nuevo_mensaje:
        message = copy.deepcopy("PASSWORD INVALID")
        return message
    else:
        message = copy.deepcopy(f"{mensaje_de_error}")

    return message

def get_basic_message(header={},payload={}):
    """Return an inititialized  messsage struct

    Args:
        header: If defined add to header
        payload: If defined add to payload

    Returns: struct initilialized
    """
    message = copy.deepcopy(_BASIC_MESSAGE)
    if not "id" in message or message["id"] == None:
        message["id"]= str(uuid.uuid4())
    if len(header) > 0:
        for k,v in header.items():
            message["header"][k]= copy.deepcopy(v)
    message["payload"] = payload
    return message

def update_message(message,id=None,status=0, header=None, payload=None,errors=None):
    """Update a BASIC_MESSAGE according to parameters

    Args:
        message: Struct to update
        id: Id to update (BASIC_MESSAGE["id"])
        status: Status to update (BASIC_MESSAGE["status"])
        header: Header to update (BASIC_MESSAGE["header"])
        payload: Payload to update (BASIC_MESSAGE["payload"])
        errors: Errors to append (BASIC_MESSAGE["errors"])

    Returns:
        Updated struct
    """
    message["status"] = status
    if id != None and len(str(id)) >0: message["id"] = id
    if payload:
        message["payload"] = payload
    if header:
        for k, v in header.items():
            message["header"][k] = copy.deepcopy(v)
    if errors and len(errors)>0:
        message["errors"] += errors

    return message


def update_message_from(message, from_message,fields=[]):
    """Update a BASIC_MESSAGE struct from another

    Args:
        message: Destination struct (to update)
        from_message: Source struct (to get the values)
        fields: List of fields to update

    Returns:
        Updated struct
    """
    for f in fields:
        if f in from_message:
            message[f]= copy.deepcopy(from_message.get(f))
    return message

def to_string(message,header=True, payload=True,errors=True):
    """BASIC_MESSAGE to string"""
    msg=f"|{dpath(message,'id','MISSING')}|"
    msg=f"{msg}{dpath(message, 'header.service', 'MISSING')}|"
    msg = f"{msg}{dpath(message, 'header.fn', 'MISSING')}|"

    msg=f"{msg}{dpath(message, 'header.user', 'MISSING')}|"
    msg=f"{msg}{dpath(message,'status','MISSING')}|"
    if errors:
        msg=f"{msg}{str(dpath(message,'errors', 'MISSING'))}|"
    else:
        msg=f"{msg}"

    if header:
        msg=f"{msg}{str(dpath(message,'header','MISSING'))}|"
    else:
        msg=f"{msg}"
    if payload:
        msg=f"{msg}{str(dpath(message,'payload', 'MISSING'))}"
    else:
        msg = f"{msg}"
    return msg
