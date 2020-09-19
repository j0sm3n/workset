""" Datos.
Gestiona todos los datos almacenados en la base de datos.

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

    - duracion(turno):
        Devuelve la duración del turno indicado.

        Forma de uso:
        >>> length('1F')
        8:21
"""

import sqlite3
from datetime import datetime


db_path = '/Users/jose/Proyectos/workdays/db.sqlite3'


def datos_agente(cf):
    """Devuelve el nombre y el id del calendario del agente según su CF.
    """
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        try:
            cursor.execute(f"SELECT agent_id, calendar FROM weekly_calendar WHERE agent_id='{cf}';")
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
        cursor.execute("SELECT * FROM weekly_agent WHERE category_id = 1")
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
        # if resultado is not None:
        if resultado:
            return True
        else:
            return False


def length(shift):
    """ Devuelve la duración del turno indicado.
    """
    pattern = '%H:%M'

    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT start, end FROM weekly_shift WHERE name='{shift}'")
        schedule = cursor.fetchone()
        start = datetime.strptime(schedule[0], pattern)
        end = datetime.strptime(schedule[1], pattern)
        return str(end - start)[:-3]


def show_shift_agent(agent, date):
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute(f"""SELECT ws.name
                          FROM weekly_agentshift AS wa
                          INNER JOIN weekly_shift AS ws
                          ON wa.shift_id = ws.id
                          WHERE wa.shift_date = '{date}'
                          AND wa.agent_id = {agent};""")
        saved_shift = cursor.fetchone()[0]
        # print(f"El agente {agent} tiene asignado el turno {saved_shift} el {date}")
    return saved_shift


def update_db_shift(agent, date, shift):
    # show_shift_agent(agent, date)
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT id FROM weekly_shift WHERE name = '{shift}';")
        shift_id = cursor.fetchone()[0]
        # print(f"El shift id nuevo es {shift_id}")
        cursor.execute(f"""UPDATE weekly_agentshift
                           SET shift_id = {shift_id}, modified = 'TRUE'
                           WHERE agent_id = {agent} AND shift_date = '{date}';""")
        db.commit()
    # show_shift_agent(agent, date)


def get_shifts():
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute("SELECT name FROM weekly_shift;")
        result = cursor.fetchall()
        return [x[0] for x in result]


def validate_shifts(shifts):
    db_shifts = get_shifts()
    new_shifts = list(set(shifts) - set(db_shifts))
    if new_shifts:
        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()
            cursor.executemany("INSERT INTO weekly_shift (name) VALUES (?);", [(a,) for a in new_shifts])


def get_calendars():
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute("SELECT agent_id, calendar FROM weekly_calendar;")
        return cursor.fetchall()