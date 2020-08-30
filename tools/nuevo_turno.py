from datetime import datetime
from .datos import agentes, existe_turno, horario_turno
from .evento_calendario import nuevo_evento

while True:
    fecha_usuario = input("Introduce la fecha [dd-mm-aaaa]: ")
    try:
        fecha = datetime.strptime(fecha_usuario, "%d-%m-%Y")
        break
    except ValueError:
        print(f'ERROR: La fecha {fecha_usuario} no es correcta.\n')

while True:
    turno = input("Introduce el turno: ")
    if existe_turno(turno):
        break
    else:
        print(f"ERROR: El turno {turno} no existe.\n")

agentes = agentes()
for n, a in enumerate(agentes):
    print(f"[{n}] -> {a[1]}")
agente = int(input("Introduce el agente: "))
agente = agentes[agente]

print(
    f"Día {fecha.strftime('%d/%m/%Y')} {agente[1]} hará el turno {turno}")

inicio, fin = horario_turno(turno)
nuevo_evento(turno,
             f'{fecha.strftime("%Y-%m-%d")}T{inicio}:00',
             f'{fecha.strftime("%Y-%m-%d")}T{fin}:00',
             agente[2])
