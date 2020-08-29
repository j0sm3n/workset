import sqlite3
import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'es_ES.utf-8')
txt_file = '/Users/jose/Proyectos/grafico-teulada/turnos.txt'
agents = [
    '677, OCHOA BAEZA, ANTONIO',
    '2560, SANJUAN IZQUIERDO, YOLANDA',
    '2082, DE LA TORRE HERRERA, RICARDO',
    '109, BIELSA NOGUES, ERNESTO',
    '2049, COLLADO MASCAROS, IVAN',
    '409, GOMEZ SEGURA, JOSE',
    '2154, LARA NAVARRO, MANUEL',
    '1651, PASTOR BERTOMEU, JAIME JUAN',
    '2076, MENDOZA RODRIGUEZ, JOSE ANTONIO',
    '597, MENA DIAZ, VICTOR',
    '2316, ESTEVE GIMENO, ENRIQUETA',
    '2586, PEREZ SANTAMARIA, MONICA',
    '159, CARMONA GARCIA, DIEGO JOSE',
    '133, BOU SERRALTA, MIGUEL ANGEL',
    '2588, LLOPES MOLINA, JUAN MANUEL',
    '2369, CABRERA GUERRERO, ENRIQUE',
    '1204, DE LAMA GONZALEZ, CARLOS',
    '1472, GOMEZ MARTIN, JAIME',
    '2210, MORALES ASENSI, ENRIQUE']
agents_num = len(agents)
months = ['JULIO 2020',
          'AGOSTO 2020',
          'SEPTIEMBRE 2020',
          'OCTUBRE 2020',
          'NOVIEMBRE 2020',
          'DICIEMBRE 2020']


def import_txt_into_bd():
    """
    Script that imports txt file with raw data into the project database
    """
    conn = sqlite3.connect('../db.sqlite3')
    cursor = conn.cursor()

    lines = (line for line in open(txt_file))
    for m in months:
        month_generator = (s.replace('\n', '').split(',') for s in lines)
        month = next(month_generator)
        for i in range(0, len(month), agents_num + 2):
            day_line = month[i:i + agents_num + 2]
            shift_date = datetime.strptime(day_line[0].replace('.', '-2020'), '%d-%b-%Y')
            for index, agent in enumerate(agents):
                cf = int(agent.split(',')[0])
                str_shift_date = shift_date.strftime('%d-%m-%Y')
                cursor.execute(f"SELECT id FROM weekly_shift WHERE name is '{day_line[2:][index]}';")
                shift_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO weekly_agentshift VALUES (null, ?, ?, ?, ?);",
                               (str_shift_date, cf, shift_id, 'FALSE'))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    import_txt_into_bd()
