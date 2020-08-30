""" Datos.
Gestiona todos los datos almacenados en turnos.db

    - nuevo_agente(cf)
        Crea un nuevo agente y, en el caso de que no exista la tabla,
        la crea y luego añade al agente.

        Forma de uso:
        >>> nuevo_agente(2076)
        Nombre del agente: Jose
        Id del calendario: blablabla@group.calendar.google.com

    - datos_agente(cf):
        Devuelve una tupla con nombre y el id del calendario del agente
        según su CF.

        Forma de uso:
        >>> datos_agente(2076)
        ('Jose', 'blablablag@group.calendar.google.com')

    - agentes():
        Devuelve una lista de tuplas con todos los datos de los agentes.

        Forma de uso:
        >>> agentes()
        [(1508, 'Itziar', 'bliblibli@group.calendar.google.com'),
        (2076, 'Jose', 'blablabla@group.calendar.google.com')]

    - horario_turno(turno)
        Devuelve dos cadenas de texto con la hora de inicio y de fin del
        turno correspondiente.

        Forma de uso:
        >>> horario_turno('1')
        ('05:21:00', '13:42:00')

    - nuevo_turno(turno):
        Crea un nuevo turno en la base de datos.

        Forma de uso:
        >>> nuevo_turno('1F')
        Introduce la hora de inicio del turno 1F [hh:mm]: 05:21
        Introduce la hora de fin del turno 1F [hh:mm]: 13:42
        Se ha creado el turno 1F.

    - duracion(turno):
        Devuelve la duración del turno indicado.

        Forma de uso:
        >>> duracion('1F')
        8:21

    - insertar_duracion():
        Introduce la duración de cada turno de trabajo en la base
        de datos.

        Forma de uso:
        >>> insertar_duracion()
"""

import os
import sqlite3
from datetime import datetime
from django.conf import settings


db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')


# def nuevo_agente(cf):
#     """Crea un nuevo agente y, en el caso de que no exista la tabla,
#     la crea y luego añade al agente.
#     """
#     nombre = input("Nombre del agente: ")
#     calendario = input("Id del calendario: ")
#
#     conexion = sqlite3.connect('turnos.db')
#     cursor = conexion.cursor()
#
#     try:
#         cursor.execute('INSERT INTO agentes VALUES (?, ?, ?);',
#                        (cf, nombre, calendario))
#         print(f"\nSe ha añadido el agente {nombre} a la base de datos.\n\n")
#     except sqlite3.OperationalError:
#         print("ERROR: No existe la tabla agentes. Creando nueva tabla...")
#         cursor.execute("""CREATE TABLE agentes (
#                 cf INTEGER(4) NOT NULL UNIQUE,
#                 nombre TEXT(20) NOT NULL,
#                 calendario TEXT(70),
#                 PRIMARY KEY(cf))""")
#         print("Se ha creado la tabla agentes.")
#         cursor.execute('INSERT INTO agentes VALUES (?, ?, ?);',
#                        (cf, nombre, calendario))
#         print(f"\nSe ha añadido el agente {nombre} a la base de datos.\n\n")
#     finally:
#         conexion.commit()
#         conexion.close()


def datos_agente(cf):
    """Devuelve el nombre y el id del calendario del agente según su CF.
    """
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        try:
            cursor.execute(f"SELECT nombre, calendario FROM agentes WHERE cf='{cf}';")
            datos_agente = cursor.fetchone()
            if datos_agente is not None:
                return datos_agente[0], datos_agente[1]
            else:
                raise sqlite3.OperationalError
        except sqlite3.OperationalError:
            print(f"\n\nERROR: El agente {cf} no existe en la base de datos.")


def agentes():
    """Devuelve una lista de tuplas con todos los datos de los agentes.
    """
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM agentes")
        agentes = cursor.fetchall()
        return agentes


def horario_turno(shift):
    """Devuelve el horario de inicio y final de cada turno de trabajo
    """

    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        try:
            cursor.execute(f"SELECT start, end FROM weekly_shift WHERE name='{shift}'")
            horario = cursor.fetchone()
            if len(horario) > 0:
                return horario[0], horario[1]
            else:
                raise sqlite3.OperationalError
        except sqlite3.OperationalError:
            print(f"\n\nERROR: El turno {shift} no existe en la base de datos.")


def existe_turno(shift):
    """ Comprueba si existe el turno en la base de datos, en cuyo caso
    devuelve True. De lo contrario devuelve False.
    """

    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM weekly_shift WHERE name='{shift}'")
        resultado = cursor.fetchone()
        if resultado is not None:
            return True
        else:
            return False


# def nuevo_turno(turno):
#     """ Crea un nuevo turno en la base de datos.
#     """
#
#     conexion = sqlite3.connect('turnos.db')
#     cursor = conexion.cursor()
#
#     # Introduce el horario de inicio y fin del turno
#     inicio = input(
#         f"\nIntroduce la hora de inicio del turno {turno} [hh:mm]: ")
#     fin = input(f"Introduce la hora de fin del turno {turno} [hh:mm]: ")
#
#     try:
#         cursor.execute('INSERT INTO turnos VALUES (?, ?, ?, ?);',
#                        (turno, inicio, fin, ''))
#         print(f"\nSe ha creado el turno {turno}.\n\n")
#     except sqlite3.OperationalError:
#         print("ERROR: No existe la tabla. Creando nueva tabla...")
#         cursor.execute("""CREATE TABLE turnos (
#                 turno TEXT(3) NOT NULL UNIQUE,
#                 inicio TEXT(8),
#                 fin TEXT(8),
#                 duracion TEXT(8),
#                 PRIMARY KEY(turno))""")
#         print("Se ha creado la tabla.")
#         cursor.execute('INSERT INTO turnos VALUES (?, ?, ?, ?);',
#                        (turno, inicio, fin, ''))
#         print(f"\nSe ha creado el turno {turno}.\n\n")
#     finally:
#         conexion.commit()
#         conexion.close()


def duracion(shift):
    """ Devuelve la duración del turno indicado.
    """
    formato = '%H:%M'

    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT start, end FROM weekly_shift WHERE name='{shift}'")
        horario = cursor.fetchone()
        inicio = datetime.strptime(horario[0], formato)
        fin = datetime.strptime(horario[1], formato)
        duracion = fin - inicio
        return str(duracion)[:-3]


# def insertar_duracion():
#     """ Introduce la duración de cada turno de trabajo en la base
#     de datos.
#     """
#     conexion = sqlite3.connect('turnos.db')
#     cursor = conexion.cursor()
#     cursor.execute("SELECT * FROM turnos")
#     turnos = cursor.fetchall()
#
#     for turno in turnos:
#         if turno[1] == '':
#             continue
#         else:
#             d = duracion(turno[0])
#             cursor.execute(
#                 f"UPDATE turnos SET duracion='{d}' WHERE turno='{turno[0]}'")
#
#     conexion.commit()
#     conexion.close()
#
#
# if __name__ == "__main__":
#     existe_turno("8")
