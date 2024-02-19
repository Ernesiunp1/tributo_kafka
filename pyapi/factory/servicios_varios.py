from .usuarios import *
import random

# lista = [u_1, u_2, u_6]
lista = [u_9]
# lista = [u_2, u_3]
# lista = [u_1, u_6]
usuario = random.choice(lista)
# ESTADO DE CUENTA (CCMA)
cuit1 = usuario["cuit"]
pwd1 = usuario["password"]
usuario = random.choice(lista)
cuit2 = usuario["cuit"]
pwd2 = usuario["password"]
usuario = random.choice(lista)
cuit3 = usuario["cuit"]
pwd3 = usuario["password"]
usuario = random.choice(lista)
cuit4 = usuario["cuit"]
pwd4 = usuario["password"]
usuario = random.choice(lista)
cuit5 = usuario["cuit"]
pwd5 = usuario["password"]
cuit8 = usuario["cuit"]
pwd8 = usuario["password"]

"============================SERVICIOS AFIP====================================="
ccma = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit1,
                'password': pwd1,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_afip.anfler_ccma.CCMA@run',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {},
    }
}

# CAPTURA DE CONSTANCIA
captura = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit4,
                'password': pwd4,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_afip.anfler_constancia_inscripcion.Constancia@get_image',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {},
    }
}

# ACTIVIDAD DE CONSTANCIA
actividad = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit5,
                'password': pwd5,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_afip.anfler_constancia_inscripcion.Constancia@get_activity',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {},
    }
}

# DIRECCION DE CONSTANCIA
direccion = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit3,
                'password': pwd3,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_afip.anfler_constancia_inscripcion.Constancia@get_address',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {},
    }
}

# CATEGORIA DE CONSTANCIA
categoria = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_afip.anfler_constancia_inscripcion.Constancia@get_category',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {},
    },
}

# VENTAS DE COPROBANTE EN LINEA
ventas1 = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit1,
                'password': pwd1,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_afip.anfler_comprobantes.Comprobantes@get_sales',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            'from': '01/09/2020',
            'to': '10/11/2020',
        },
    },
}

# VENTAS DE MIS COPROBANTE
ventas2 = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_afip.anfler_mis_comprobantes.MisComprobantes@get_sales',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            'from': '01/09/2020',
            'to': '10/11/2020',
        },
    }
}

compras = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_afip.anfler_mis_comprobantes.MisComprobantes@get_purchases',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            'from': '01/09/2020',
            'to': '10/11/2020',
        },
    }
}

# MONOTRIBUTO RECATEGORIZACION
recategorizacion = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_fip.anfler_recategorizacion.Recategorizacion@run',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            'monto_facturado': None,
            'local': 'no|si',
            'Energía eléctrica consumida': 154,
            'Superficie afectada': 54,
            'alquilado': "no|si",
            'Alquileres correspondientes': 80000,
            'cuantos inmuebles alquila': "0 (cero)|1 (uno)|2 (dos)",
            'locadores': [209568043, 2095680]  # CUITS
        },
    }
}

# AFIP MONOTRIBUTO MODIFICACION
modificacion = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_fip.anfler_modificacion.Modificacion@modificar',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            'componente_provincial': 'no',  # si|no
            'actividad en mas de una provincia': "no",
            'como_vas_a_trabajar': 'VOY A REALIZAR TRABAJO INDEPENDIENTE',  # 'VOY A REALIZAR TRABAJO INDEPENDIENTE'|'COMO MIEMBRO DE UNA COOPERATIVA'|'COMO TRABAJADOR PROMOVIDO'
            'mes_aplicacion': 'ACTUAL',  # 'ACTUAL' | 'PROXIMO'
            'facturacion_anual': 650000,  # integer
            'local': 'no',  # 'si'|'no'
            'consumo_anual_energia': 55,  # integer
            'superficie_afectada': 45,  # integer
            'alquilado': 'no',  # 'si'|'no'
            'monto_anual_alquiler': 45000,  # integer
            'jubilacion': 'EMPLEADO EN RELACION DE DEPENDENCIA',  # 'TRABAJADOR ACTIVO'|'EMPLEADO EN RELACION DE DEPENDENCIA'|'JUBILADO'|'APORTO A UNA CAJA PREVISIONAL'|'LOCADOR DE BIENES MUEBLES O INMUEBLES'
            'ley': None,  # "None|'24.241'|'18.038/8'",
            'cuit_empleador': 30663363014,  # CUIT
            'cuit_caja': 34123456789,  # CUIT
            'codigo_obra_social': "000406",  # integer
            'sumar_aportes_de_conyuge': 'no',  # 'si'|'no'
            'cuil_conyuge': 20333333334,  # CUIT
            'cuil_familiar_adicional':
                ((27000000017, 'Cónyuge'),  # "'Cónyuge'|'Hijo/a'|'Menor/Tutelado'"
                 (27111111149, 'Hijo/a'),
                 (27222222290, 'Menor/Tutelado'))  # tuple of tuples with (cuit, rel)
        },
    }
}

baja = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_fip.anfler_modificacion.Modificacion@baja',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "periodo": '05/2021',  # 'mes/año',
            "modo_baja": "cese"  # "cese|renuncia|exclusion"
        },
    }
}

alta_monotributo = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': 20956804354,
                'password': "CIv16953524a",
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_fip.anfler_modificacion.Modificacion@alta',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            'componente_provincial': 'si',  # si|no
            'actividad en mas de una provincia': 'no',  # si|no
            'como_vas_a_trabajar': 'VOY A REALIZAR TRABAJO INDEPENDIENTE',  # 'VOY A REALIZAR TRABAJO INDEPENDIENTE'|'COMO MIEMBRO DE UNA COOPERATIVA'|'COMO TRABAJADOR PROMOVIDO'
            'mes_aplicacion': 'ACTUAL',  # 'ACTUAL' | 'PROXIMO'
            'facturacion_anual': 360000,  # integer
            'local': 'si',  # "'si'|'no'"
            'superficie_afectada': 45,  # integer
            'alquilado': 'no',  # "'si'|'no'"
            'monto_anual_alquiler': 317750,  # integer
            'jubilacion': 'TRABAJADOR ACTIVO',  # "'TRABAJADOR ACTIVO'|'EMPLEADO EN RELACION DE DEPENDENCIA'|'JUBILADO'|'APORTO A UNA CAJA PREVISIONAL'|'LOCADOR DE BIENES MUEBLES O INMUEBLES'",
            'ley': None,  # "None|'24.241'|'18.038/8'"
            'cuit_empleador': None,  # CUIT
            'cuit_caja': None,  # CUIT
            'codigo_obra_social': "402202",  # integer
            'sumar_aportes_de_conyuge': 'no',  # "'si'|'no'"
            'cuil_conyuge': None,  # CUIT
            'cuil_familiar_adicional': None, # ((2045698354, 'Hijo/a'), (209555664, 'Cónyuge'))  # tuple of tuples with (cuit, rel) "'Cónyuge'|'Hijo/a'|'Menor/Tutelado'"
        },
    }
}

alta_monotributo_simplificado = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': 27345025443,
                'password': "Angeles2022",
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_fip.anfler_modificacion.Modificacion@alta',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "ley": None,
            "local": "si",
            "alquilado": "no",
            "cuit_caja": None,
            "jubilacion": "TRABAJADOR ACTIVO",
            "cuil_conyuge": None,
            "cuit_empleador": None,
            "mes_aplicacion": "ACTUAL",
            "facturacion_anual": 1,
            "codigo_obra_social": "400602",
            "como_vas_a_trabajar": "VOY A REALIZAR TRABAJO INDEPENDIENTE",
            "superficie_afectada": 45,
            "monto_anual_alquiler": 317750,
            "componente_provincial": "si",
            "consumo_anual_energia": 3330,
            "cuil_familiar_adicional": None,
            "sumar_aportes_de_conyuge": "no",
            "actividad en mas de una provincia": "no"
            },
    }
}

vep_mensual = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_fip.anfler_vep.Vep@mensual',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "red_pago": 'Red Link'  # 'Red Link|Pago mis cuentas|Interbanking|XN Group',
        },
    }
}

vep_total = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_fip.anfler_vep.Vep@total',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "red_pago": 'Red Link'  # 'Red Link|Pago mis cuentas|Interbanking|XN Group',
        },
    }
}

# VALIDATE USER AND PWD
validate_usr_pwd = {
        'message': {
            'status': 0,
            'errors': [],
            'id': '1234567890',
            'header': {
                'auth': {
                    'codif': 0,
                    'cuit': cuit2,
                    'password': pwd2,
                    'type': 'basic'
                },
                'job_service': "afip",
                'fn': 'anfler_afip.anfler_validate_password.Validate@run',
                'offset': 0,
                'partition': 0
            },
            'payload': {},
        }
}

"============================SERVICIOS SIFERE==================================="
# SIFERE JURISDICCION
sifere_jurisdiccion = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_afip.anfler_sifere_consultas.SifereConsultas@get_jurisdiccion',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {},
    },
}

sifere_vep = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_afip.anfler_sifere_ddjj.SifereDDJJ@vep',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "cuit_to_vep": 20123456789,  # cuit a escoger para generar el vep
            "anticipo": "202004 - 0",  # formato: año|mes - tipo
            "medio_de_pago": "BANELCO" # LINK|BANELCO|INTERBANKING
        },
    },
}

descarga_cm03 = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_afip.anfler_sifere_ddjj.SifereDDJJ@descarga_cm03',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "cuit_to_vep": cuit2,  # cuit a escoger para generar el vep
            "anticipo": "202004 - 0",  # formato: año|mes - tipo
        },
    },
}

descarga_cm05 = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_afip.anfler_sifere_ddjj.SifereDDJJ@descarga_cm05',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "cuit_to_vep": cuit2,  # cuit a escoger para generar el vep
            "anticipo": None,  # "202001 - 0" formato: año|mes - tipo
        },
    },
}

sifere_saldo_favor = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_afip.anfler_sifere_ddjj.SifereDDJJ@saldo_favor',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "cuit_to_vep": cuit2,  # cuit a escoger para generar el vep
            "anticipo": "202002 - 0",  # formato: año|mes - tipo
        },
    },
}
coeficientes_unificados_cm05 = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_afip.anfler_sifere_ddjj.SifereDDJJ@coeficientes_unificados_cm05',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "cuit_to_vep": cuit2,  # cuit a escoger para continuar
            "anticipo": None,  # formato: None| añomes(202105) - tipo
        },
    },
}
ddjj_sifere = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_afip.anfler_sifere_ddjj.SifereDDJJ@ddjj',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "cuit_to_vep": cuit2,  # cuit a escoger para continuar
            "anio": 2021,  # yyyy
            "mes": "mayo",  # enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre
            "actividades": [
                {
                    "cod_actividad": "822009",
                    "monto_imponible": 400
                },
                {
                    "cod_actividad": "822001",
                    "monto_imponible": 500
                }
            ],  # lista de diccionarios [{"cod_actividad": str, "monto_imponible": float}, {"cod_actividad": str, "monto_imponible": float}]
            "jurisdicciones": {
                "901 CAPITAL FEDERAL": {
                    "base_imponible": 31.5,
                    "ingresos_no_gravados": 0,
                    "ingresos_exentos": 0,
                    "actividades": {
                        "741000": {
                            "alicuota": 2
                        },
                        "749001": {
                            "alicuota": 3
                        },
                    },
                    "saldo_favor": {
                        "periodo_anio": 2021,
                        "periodo_mes": "febrero", # enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre
                        "monto": 450
                    }
                },
                "902 BUENOS AIRES": {
                    "base_imponible": 868.5,
                    "ingresos_no_gravados": 0,
                    "ingresos_exentos": 0,
                    "actividades": {
                        "822001": {
                            "alicuota": 1.5
                        },
                        "822009": {
                            "alicuota": 1.5
                        }
                    },
                    "saldo_favor": {
                        "periodo_anio": 2021,
                        "periodo_mes": "enero", # enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre
                        "monto": 450
                    }
                }
            },  # diccionario donde la key es el nombre completo de la jurisdiccion como aparece en SIFERE y contiene otro diccionario con la estructura para declarar las alicuotas en cada jurisdiccion
            "firmante": {
                "nombre": "nombre",
                "apellido": "apellido",
                "email": "email@a.com",
                "cuit": "20123456789"
            },
            "presentar": {
                "presentar": 1,  # bool 0->No; 1->Si
                "anticipo": "202105 - 1"  # el formato es obligatorio, debe haber un espacio en blanco antes y despues del guion
                   }
        },
    },
}


"============================SERVICIOS ARBA====================================="

estado_deuda = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "arba",
            'fn': 'anfler_arba.anfler_ccma.CCMA@resume',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {},
    }
}

saldo_favor = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "arba",
            'fn': 'anfler_arba.anfler_ccma.CCMA@positive_balance',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {},
    }
}

ddjj_arba = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "arba",
            'fn': 'anfler_arba.anfler_iibb.IIBB@presentacion',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "regimen": "Mensual",  # "Mensual|Bimestral"
            "anio": 2021,
            "mes": 5,
            "monto_imponible": "620",
            "editar_alicuota": True,
            "nueva_alicuota": "4,00",  # "3,50|4,00|4,50|0,00"
        },
    }
}

vep_iibb_arba = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit8,
                'password': pwd8,
                'type': 'basic'
            },
            'job_service': "afip",
            'fn': 'anfler_arba.anfler_ccma.CCMA@vep',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "red_pago": 'Pago mis cuentas'  # 'Link|Pago mis cuentas|Interbanking',
        },
    }
}

descargar_retenc_percep = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "arba",
            'fn': 'anfler_arba.anfler_iibb.IIBB@descargar_retenc_percep',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "rol": "Contribuyente de Ingresos Brutos", # "Contribuyente de Ingresos Brutos|Contribuyente"
            "anio": "2021",
            "mes": "02"
        },
    }
}

liquidacion_mensual = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "arba",
            'fn': 'anfler_arba.anfler_iibb.IIBB@liquidacion_mensual',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "anio": "2021",
            "mes/bimestre": "2"
        },
    }
}

# Servicios AGIP

retenciones_percepciones = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "agip",
            'fn': 'anfler_agip.anfler_arciba.Arciba@retenciones_percepciones',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "ano_desde": 2020,
            "ano_hasta": 2021,
            "mes_desde": "ene",  # ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic
            "mes_hasta": "may",  # ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic
        },
    },
}

saldo_favor_agip = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "agip",
            'fn': 'anfler_agip.anfler_esicol.Esicol@saldo_favor',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {},
    },
}

descarga_ddjj_agip = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "agip",
            'fn': 'anfler_agip.anfler_esicol.Esicol@descarga_ddjj',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "periodo": "2021-03"  # formato yyyy-mm
        },
    },
}

vep_agip = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "agip",
            'fn': 'anfler_agip.anfler_esicol.Esicol@vep',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "periodo": "2021-05",  # formato yyyy-mm
            "medio_pago": "interbanking"  # pagomiscuentas|interbanking|link
        },
    },
}

ddjj_agip = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "agip",
            'fn': 'anfler_agip.anfler_esicol.Esicol@ddjj',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {
            "mes": "junio",  # enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre
            "anio": "2021",
            "actividades": {
                1: {
                    "codigo": "960990",
                    "base_imponible": 155,
                    "alicuota": 3.75,
                    "observacion": "Concepto que desea aclarar, obligatorio para algunas actividades"
                },
                2: {
                    "codigo": "960990",
                    "base_imponible": 165,
                    "alicuota": 0
                }
            },
            "saldos_favor": [{"importe": 85, "mes": "Marzo", "anio": 2020}],  # None|list of dicts [{"importe: int, "mes": str, "anio": str}]
            "retenciones_percepciones": {
                "txt_retenciones": None,
                "txt_percepcions": None,
                "txt_retenciones_bancarias": None,
                "txt_percepcions_bancarias": None,
            }
        },
    },
}

deuda_agip = {
    'message': {
        'status': 0,
        'errors': [],
        'id': '1234567890',
        'header': {
            'auth': {
                'codif': 0,
                'cuit': cuit2,
                'password': pwd2,
                'type': 'basic'
            },
            'job_service': "agip",
            'fn': 'anfler_agip.anfler_esicol.Esicol@deuda',
            'key': None,
            'offset': 0,
            'partition': 0
        },
        'payload': {},
    },
}
