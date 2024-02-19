"""Routes for /"""
import random
from datetime import datetime

from fastapi import (
       APIRouter,
       Depends,
       FastAPI,
       HTTPException
)
import app.anfler.api.api_schemas as api_schemas
import app.anfler.api.deps as deps
import anfler.util.log.lw as lw

from app.anfler.api import api_security


_log= lw.get_logger("anfler.api.default")

router = APIRouter(tags=["default"])

# ---------------------------------------------------------------------------
#   Route
# ---------------------------------------------------------------------------
@router.get("/me",response_model=api_schemas.Me)
def get_current_user(token_data = Depends(api_security.get_token_data)):
    return {"token_data": token_data, "datetime_utc": datetime.utcnow() }

# ---------------------------------------------------------------------------
#   Route
# ---------------------------------------------------------------------------
QUOTES=["No te tomes la vida demasiado en serio. No saldrás de ella con vida (Elbert Hubbard)",
       "Tener la conciencia limpia es señal de mala memoria (Steven Wright)",
       "Me gustan los largos paseos, especialmente cuando los toman gente molesta (Fred Allen)",
       "Creo que he encontrado el eslabón perdido entre el animal y el hombre civilizado. Somos nosotros (Konrad Lorenz)",
       "Todo es divertido, con tal de que le suceda a otra persona (Will Rogers)",
       "Siempre recuerda que tú eres único. Absolutamente igual que todos los demás (Margaret Mead)",
       "Estoy seguro de que el universo está lleno de vida inteligente. Simplemente ha sido demasiado inteligente para venir aquí (Arthur C. Clark)",
       "Sólo hay dos cosas infinitas: el universo y la estupidez humana. Y no estoy tan seguro de la primera (Albert Einstein)",
       "Un experto es alguien que te explica algo sencillo de forma confusa de tal manera que te hace pensar que la confusión sea culpa tuya (William Castle)",
       "Claro que lo entiendo. Incluso un niño de cinco años podría entenderlo. ¡Qué me traigan un niño de cinco años! (Groucho Marx)",
       "Fuera del perro, un libro es probablemente el mejor amigo del hombre, y dentro del perro probablemente está demasiado oscuro para leer (Groucho Marx)",
       "Un arqueólogo es el mejor esposo que una mujer podría tener. Cuando más envejece ella, más interesado está él en ella. (Agatha Christie)",
       "Trabajar no es malo, lo malo es tener que trabajar (Don Ramón)",
       "La edad es algo que no importa, a menos que sea usted un queso (Luis Buñuel)",
       "¡Si Dios tan solo me diera una clara señal! Como hacer un gran depósito a mi nombre en un banco suizo (Woody Allen)",
       "Una celebridad es una persona que trabaja toda su vida para ser conocida, entonces se pone gafas oscuras para evitar ser reconocida (Fred Allen)",
       "¡Odio las tareas del hogar! Haces las camas, limpias los platos y seis meses después tienes que empezar de nuevo (Joan Rivers)",
       "Suelo cocinar con vino, a veces incluso se lo agrego a la comida (W.C. Fields)",
       "El dinero no da la felicidad, pero procura una sensación tan parecida que necesita un especialista muy avanzado para verificar la diferencia (Woody Allen)",
       "Mi mujer y yo fuimos felices durante 20 años. Luego, nos conocimos (Rodney Dangerfield)",
       "La vida es dura. Después de todo, te mata (Katherine Hepburn)",
       "Cuando la vida te da limones, arrójaselos a alguien a los ojos (Cathy Guisewite)",
       "Seguramente existen muchas razones para los divorcios, pero la principal es y será la boda (Jerry Lewis)",
       "Por supuesto que debes casarte. Si consigues una buena esposa, te convertirás en alguien feliz. Si consigues una mala, te convertirás en filósofo (Sócrates)",
       "Si pudieras patear en el trasero al responsable de casi todos tus problemas, no podrías sentarte por un mes (Theodore Roosevelt)",
       "Nunca dejes para mañana lo que puedas hacer pasado mañana (Mark Twain)",
       "Mi idea de una persona agradable es una persona que está de acuerdo conmigo (Benjamin Disraeli)",
       "Me gustaría tomarte en serio, pero hacerlo sería ofender tu inteligencia (George Bernard Shaw)",
       "Un hombre exitoso es uno que gana más dinero del que su mujer puede gastar. Una mujer exitosa es una que puede encontrar un hombre así (Lana Turner)",
       "Nunca olvida una cara, pero en su caso estaré encantado de hacer una excepción (Groucho Marx)",
       "Ríe y el mundo reirá contigo, ronca y dormirás solo (Anthony Burgess)",
       "Encuentro la televisión muy educativa. Cada vez que alguien la enciende, me retiro a otra habitación y leo un libro (Groucho Marx)",
       "El sexo es como el mus: si no tienes buena pareja… más te vale tener una buena mano (Woody Allen)",
       "Esas personas que creen que lo saben todo son una verdadera molestia para aquellos que de verdad lo sabemos todo (Isaac Asimov)",
       "El amor nunca muere de hambre; con frecuencia, de indigestión (Ninon de Lenclos)",
       "Santa Claus tenía la idea correcta: visita a la gente una vez al año (Víctor Borge)",
       "Para volver a ser joven yo haría cualquier cosa en el mundo excepto ejercicio, levantarme temprano o ser respetable (Oscar Wilde)",
       "Mis plantas de plástica murieron porque no aparenté regarlas (Mitch Hedberg)",
       "Me puse a dieta, juré que no volvería a beber ni a comer con exceso y en catorce días había perdido dos semanas (Joe E. Lewis)",
       "Hago ejercicio a menudo. Mira, precisamente ayer tomé el desayuno en la cama (Oscar Wilde)"
       ]
@router.get("/")
async def get_default():
    """Default / route"""
    return {"message": "Ops, pending...",
            "quote": random.choice(QUOTES)
            }
