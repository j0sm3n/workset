from django.http import HttpResponse


def index(request):
    return HttpResponse("""
        <h1>Gestión de turnos de trabajo</h1>
    """)

def weekly(request):
    return HttpResponse("""
        <h1>Turnos semanales</h1>
    """)

def weekly_agent(request):
    return HttpResponse("""
        <h1>Turnos semanales del agente</h1>
    """)