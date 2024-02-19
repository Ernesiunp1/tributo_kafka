import json

BASIC_MESSAGE = {
    "id": '08b9c104-ae6a-45cd-b774-634fc2a04f14',
    "header": {
        "key": None,
        "fn": "anfler_afip.anfler_constancia_inscripcion.Constancia@get_address",
        "cuit": 1321356,
        "password": "ad53f135as",
        "from": "01/10/2020",
        "to": "28/11/2020"
    },
    "payload": {
        "i":
            {
                "from": "01/10/2020",
                "to": "28/11/2020"
            }
    },
    "status": 0,
    "errors": []
}

mensaje_kafka = {
    "fn": {"organismo": "anfler_afip",
           "tramite": "ccma",
           "prueba": "anfler_afip.anfler_constancia_inscripcion.Constancia@get_address"
           },
    "data": {
        "cuit": 2354,
        "password": "CIv24b",
        "from": "01/10/2020",
        "to": "01/11/2020"
    }
}


msg_kafka = {
    "data": {
        "cuit": "2",
        "password": "",
        "from": "01/01/2020",
        "to": "10/11/2020"
    },
    "payload": {
        "dato1": "abc",
        "dato3": "123",
        "dato4": "blabla"
    },
    "metodo": "metodoA"
}

from_kafka = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': 2,
                'password': 'b',
                'type': 'basic'
            },
            'fn': 'anfler_afip.anfler_ccma.CCMA@run',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            'from': '01/09/2020',
            'to': '10/11/2020',
        },
    },
    "browser": "chrome",
    "t_s": 0.5
}

output_model = {
    'messages': {
        'status': 0,
        'errors': [],
        'header': {
            'auth': {
                'codif': 0,
                'cuit': 0,
                'password': '',
                'type': 'basic'
            },
            'fn': '',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'id': None,
        'payload': {
            'data': ''
        }
    }
}


msg_kafka_json = json.dumps(msg_kafka)
