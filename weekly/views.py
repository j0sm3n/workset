from django.shortcuts import HttpResponse, render
from weekly.models import Agent


def index(request):
    return render(request, 'weekly/index.html')

def weekly(request):
    return render(request, 'weekly/weekly.html')

def weekly_agent(request):
    return render(request, 'weekly/weekly-agent.html')

def new_agent(request, cf, name, surnames, category, residence):
    agent = Agent(
        cf = cf,
        name = name,
        surnames = surnames,
        category = category,
        residence = residence
    )

    agent.save()

    return HttpResponse(f"Creado el agente <strong>{agent.cf} {agent.name} {agent.surnames}</strong>")

def agent(request, cf):
    try:
        agent = Agent.objects.get(pk=cf)
        response = f"Agente: {cf} {agent.name.title()} {agent.surnames.title()}"
    except:
        response = "<strong>Agente no encontrado</strong>"
    return HttpResponse(response)

def agents(request):
    agents = Agent.objects.all()

    return render(request, 'weekly/agents.html', {'agents': agents})