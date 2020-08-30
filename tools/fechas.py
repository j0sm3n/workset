"""Fechas

    Devuelve una lista de cadenas de texto con las fechas de la próxima
    semana con respecto a una fecha.

    Forma de uso:
    >>> prox_semana('2020-05-25')
    ['2020-05-25', '2020-05-26', '2020-05-27', '2020-05-28', '2020-05-29',
    '2020-05-30', '2020-05-31']
"""

import locale
import datetime


locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")


def prox_semana(lunes):
    """ Devuelve una lista de cadenas de texto con las fechas de la próxima
    semana con respecto a la fecha pasada.
    """
    prox_semana = []

    for d in range(7):
        dia = lunes + datetime.timedelta(d)
        prox_semana.append(dia.strftime('%Y-%m-%d'))

    return prox_semana


# Deja de ser útil. Conservo de momento.
def prox_dia(fecha, dia_semana):
    """ Devuelve el próximo día de la semana con respecto a la fecha pasada.
    Ejemplo:
    >>> prox_dia(datetime.date(2020, 5, 7), 2)
    2020-05-13
    """
    faltan_dias = (dia_semana - fecha.weekday()) % 7
    return fecha + datetime.timedelta(days=faltan_dias)


# def prox_semana():
#     """ Devuelve una lista de cadenas de texto con las fechas de la próxima
#     semana con respecto a hoy.
#     """
#     hoy = datetime.date.today()
#     prox_lunes = prox_dia(hoy, 0)
#     prox_semana = []

#     for d in range(7):
#         dia = prox_lunes + datetime.timedelta(d)
#         prox_semana.append(dia.strftime('%Y-%m-%d'))

#     return prox_semana
