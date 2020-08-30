from .datos import agentes, horario_turno
from .datos_excel import fecha_grafico, turnos_semana
from .evento_calendario import nuevo_evento
from .fechas import prox_semana


def main(excel_file):

    hoja = 'G_BENIDORM'
    f_grafico = fecha_grafico(excel_file)
    semana = prox_semana(f_grafico)
    lunes = f'{semana[0][8:]}-{semana[0][5:7]}'
    domingo = f'{semana[-1][8:]}-{semana[-1][5:7]}'
    agents = agentes()

    for agente in agents:
        turnos = turnos_semana(excel_file, hoja, agente[0])

        # DEBUG: Imprime por pantalla
        print(f"\n\n\tTurnos de {agente[1]}")
        print(f"\tSemana del {lunes} al {domingo}\n")
        for i, dia in enumerate(semana):
            try:
                inicio, fin = horario_turno(turnos[i])
            except TypeError:
                inicio, fin = '', ''
            if inicio != '':
                print(f"\t{dia} -> Turno {turnos[i]}, de {inicio} a {fin}")
            else:
                print(f"\t{dia} -> Turno {turnos[i]}")

        print()

        # Crea un evento en el calendadio por cada turno de trabajo
        for i, dia in enumerate(semana):
            try:
                inicio, fin = horario_turno(turnos[i])
            except TypeError:
                inicio, fin = '', ''
            if inicio != '':
                nuevo_evento(turnos[i],
                             f'{dia}T{inicio}:00',
                             f'{dia}T{fin}:00',
                             agente[2])


def save_week_shifts(excel_file):
    main(excel_file)
