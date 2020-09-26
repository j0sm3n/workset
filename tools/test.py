import csv
import os
from .manage_db import agentes, horario_turno, validate_shifts, show_shift_agent, update_db_shift, get_calendars
from .datos_excel import fecha_grafico, turnos_semana
from .evento_calendario import nuevo_evento
from .fechas import prox_semana


def create_calendar_events(excel_file):
    """Creates events in google calendar"""

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

        # Creates events in work google calendar
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


def excel_to_db(excel_file):
    """Modify the shifts saved in the database with those present in the excel file.
    At the end, it calls method create_csv with the data extracted from the excel file."""

    monday = fecha_grafico(excel_file)
    week_dates = prox_semana(monday)
    agents = agentes()
    csv_data = [week_dates]
    for agent in agents:
        agent_shifts = turnos_semana(excel_file, agent[0])
        csv_data.append([agent[0], agent[2].title() + ', ' + agent[1].title()])
        for shift in agent_shifts:
            csv_data[-1].append(shift)
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
    create_csv(csv_data)


def create_csv(csv_data):
    """Create an excel file with the information extracted from the excel file to be read when
    listing the weekly chart"""

    csv_path = '/Users/jose/Proyectos/workdays/media/this_week.csv'
    csv_old = '/Users/jose/Proyectos/workdays/media/last_week.csv'
    if os.path.exists(csv_path):
        os.replace(csv_path, csv_old)
    with open(csv_path, mode='w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(csv_data)


if __name__ == '__main__':
    excel_to_db('/Users/jose/Downloads/GSEMANAL20.xlsx')
