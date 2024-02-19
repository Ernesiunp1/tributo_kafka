"""Constant
"""
from collections import namedtuple


# ---------------------------------------------------------------------------
#   Jobs state
#   For anfler.db and anfler.api
# ---------------------------------------------------------------------------
__JOBS_STATE = namedtuple("JOBS_STATE", ["PENDING", "FINISHED"])
JOBS_STATE = __JOBS_STATE(PENDING=0, FINISHED=1)
DEFAULT_EMPTY = "UNKNOWN"

# ---------------------------------------------------------------------------
#   Jobs Services: these values maps to tables (jobs_afip,....)
#   This value must be defined in BASIC_MESSAGE.header.job_service
# ---------------------------------------------------------------------------
__ENTITIES=namedtuple("ENTITIES", ["AFIP", "ARBA", "AGIP","ADMIN", "ALL"])
ENTITIES = __ENTITIES(AFIP="afip",ARBA="arba",AGIP="agip", ADMIN="admin", ALL="")

# ---------------------------------------------------------------------------
#   Basic Errors
#   Some errors code as constant
# ---------------------------------------------------------------------------
__ERROS_CODE = namedtuple("ERRORS_CDDE", ["OK", "KO",
                                          "GENERIC_ERROR1",
                                          "GENERIC_ERROR2",
                                          "GENERIC_ERROR3",
                                          "TIMEOUT"])
ERRORS_CDDE = __ERROS_CODE(OK=0,
                           KO=-1,
                           GENERIC_ERROR1=-2,
                           GENERIC_ERROR2=-3,
                           GENERIC_ERROR3=-4,
                           TIMEOUT=-5)
