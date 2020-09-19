from .manage_db import agentes, horario_turno, validate_shifts, show_shift_agent, update_db_shift, get_calendars
from .datos_excel import fecha_grafico, turnos_semana
from .evento_calendario import nuevo_evento
from .fechas import prox_semana


db_path = '/Users/jose/Proyectos/workdays/db.sqlite3'


def save_week_shifts(excel_file):

    start_day = fecha_grafico(excel_file)
    week = prox_semana(start_day)
    monday = f'{week[0][8:]}-{week[0][5:7]}'
    sunday = f'{week[-1][8:]}-{week[-1][5:7]}'
    agents_calendars = get_calendars()

    for agent_calendar in agents_calendars:
        shifts = turnos_semana(excel_file, agent_calendar[0])

        # DEBUG: Imprime por pantalla
        print(f"\n\n\tTurnos de {agent_calendar[1]}")
        print(f"\tSemana del {monday} al {sunday}\n")
        for i, date in enumerate(week):
            try:
                start, end = horario_turno(shifts[i])
            except TypeError:
                start, end = '', ''
            # if inicio != '':
            if start:
                print(f"\t{date} -> Turno {shifts[i]}, de {start} a {end}")
            else:
                print(f"\t{date} -> Turno {shifts[i]}")

        print()
        # -- Fin DEBUG

        # Crea un evento en el calendadio por cada turno de trabajo
        for i, date in enumerate(week):
            try:
                start, end = horario_turno(shifts[i])
            except TypeError:
                start, end = '', ''
            # if inicio != '':
            if start:
                nuevo_evento(shifts[i],
                             f'{date}T{start}:00',
                             f'{date}T{end}:00',
                             agent_calendar[1])


def xls2db(excel_file):
    monday = fecha_grafico(excel_file)
    week_dates = prox_semana(monday)
    agents = agentes()
    for agent in agents:
        agent_shifts = turnos_semana(excel_file, agent[0])
        validate_shifts(agent_shifts)
        for i, day in enumerate(week_dates):
            try:
                saved_shift = show_shift_agent(agent[0], day)
                if saved_shift[0] != agent_shifts[i]:
                    update_db_shift(agent[0], day, agent_shifts[i])
                    print(f"Actualizado: {day} {agent[0]} {saved_shift[0]} -> {agent_shifts[i]}")
            except Exception as e:
                print(f"Algo raro ha pasado: {e}")
                print(f"\t- {day} {agent[0]} {saved_shift[0]} -> {agent_shifts[i]}")


# if __name__ == '__main__':
#     xls2db('/Users/jose/Downloads/GSEMANAL20.xlsx')
    # update_db_shift(109, '2020-09-14', 'V')
