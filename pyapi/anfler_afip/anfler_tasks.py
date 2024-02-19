from peewee import *
from datetime import date
import datetime
import os
import shutil

now = datetime.datetime.now()

dia = now.day
mes = now.month
anio = now.year


db_path = f"/app/logs/tasks/{mes}/{dia}.db"

class Tasks(Model):
    task_id  = AutoField()
    fecha    = date.today()
    job_id   = CharField()
    servicio = CharField()
    status   = CharField()
    error    = CharField()

# SI NO EXISTE EL PATH A LA BASE DE DATOS SE CREA
if not os.path.exists(db_path):
    directorio = f"/app/logs/tasks/{mes}"
    if not os.path.exists(directorio):
        os.makedirs(directorio)

    with open(db_path, 'w')as file:
        file.close()

    # GENERA LA INSTANCIA DE LA DB SE CONECTA Y CREA LA TABLA
    db = SqliteDatabase(db_path)
    db.connect(['Tasks'])
    db.bind([Tasks])
    db.create_tables([Tasks])


# SI EXISTE EL PATH A LA BASE DE DATOS 
# CREA LA INSTANCIA, SE CONECTA Y CREA LA TABLA
db = SqliteDatabase(db_path)
db.connect(['Tasks'])
db.bind([Tasks])
db.create_tables([Tasks])



def create_task(job_id, servicio, task_status="inicializado", task_error="None"):

    new_task = Tasks(job_id=job_id, servicio=servicio, status=task_status, error=task_error)
    new_task.save()


def update_task(job_id, task_status, task_error='no error'):

    Tasks.update(status=task_status).where(Tasks.job_id == job_id).execute()
    Tasks.update(error=task_error).where(Tasks.job_id == job_id).execute()


def imprimir_tasks(db_path):

    """ FUNCION PARA LLAMAR Y VER LOS DATOS DE LA TABLA  DESDE LA TERMINAL
    SE DEBE LLAMAR DESDE EL ARCHIVO DONDE EXISTE
    EL PARAMETRO db_path es el path completo de la tabla
    :return en la terminal la tabla
    """

    db = SqliteDatabase(db_path)
    db.connect()
    db.bind([Tasks])

    for tasks in Tasks.select():

        print(f" id: {tasks.task_id}, "
              f"fecha: {tasks.fecha}, "
              f"job_id: {tasks.job_id}, "
              f"servicio: {tasks.servicio}, "
              f"status: {tasks.status}, "
              f"error: {tasks.error}"
              )


directorio_borrado = f'/app/logs/tasks'

meses = os.listdir(directorio_borrado)

for mes in meses:
    mes_vencido = str(now.month - 2)
    if mes_vencido in os.listdir(directorio_borrado):
        path = os.path.join(directorio_borrado, mes_vencido)
        shutil.rmtree(path)




# TIPOS DE MENSAJES CREADO EN LA BASE DE DATOS: 

# SE CREA INSTANCIA EN LA BASE DE DATOS TASK.PY
#            create_task(job_id=self._id,
#                        servicio='ccma',
#                        task_status="init-not-end",
#                        task_error='not-error')


# SE ACTUALIZA REGISTRO EN BASE DE DATOS TASK.PY COMO TAREA EXITOSA
#                update_task(job_id=self._id,
#                        task_status="end-successful",
#                        task_error="not-error")


# SE ACTUALIZA REGISTRO EN BASE DE DATOS TASK.PY COMO TAREA FALLIDA
#            update_task(job_id=self._id,
#                        task_status="failed",
#                        task_error=e)
