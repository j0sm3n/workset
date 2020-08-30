import os, shutil
import datetime, locale
from django.shortcuts import HttpResponse, render, redirect
from django.contrib import messages
from django.conf import settings
from weekly.models import Agent, Residence, Category, Document
from weekly.forms import AgentForm, DocumentForm
from tools.datos_excel import rename_doc, turnos_semana, fecha_grafico
from tools.test import save_week_shifts


locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")

def index(request):

    documents = Document.objects.order_by('-document')
    return render(request, 'weekly/index.html', {
        'title': 'Gestión de turnos',
        'documents': documents,
    })


def weekly(request):

    document = Document.objects.latest('document')
    agnts = Agent.objects.all()
    monday = fecha_grafico(document.document.path)
    sunday = monday + datetime.timedelta(6)
    caption = f"Semana del {monday.strftime('%d-%b')} al {sunday.strftime('%d-%b')}"
    agents_shifts = []
    for agnt in agnts:
        agnt_name = f'{agnt.surnames.title()}, {agnt.name.title()}'
        agnt_shifts = {'name': agnt_name,
                       'shifts': turnos_semana(document.document.path, 'G_BENIDORM', agnt.cf)}
        agents_shifts.append(agnt_shifts)

    return render(request, 'weekly/weekly.html', {
        'title': 'Turnos semanales',
        'agents_shifts': agents_shifts,
        'caption': caption
    })


def weekly_agent(request):
    return render(request, 'weekly/weekly-agent.html', {
        'title': 'Turnos del agente'
    })


def agent(request, cf):
    try:
        agnt = Agent.objects.get(pk=cf)
    except:
        return render(request, 'weekly/weekly-agent.html', {
            'title': "Agente no encontrado", })
    return render(request, 'weekly/weekly-agent.html', {
        'title': 'Turnos del agente',
        'cf': agnt.cf,
        'name': agnt.name,
        'surnames': agnt.surnames,
    })


def agents(request):
    agnts = Agent.objects.order_by('cf')

    return render(request, 'weekly/agents.html', {
        'title': 'Listado de agentes',
        'agents': agnts,
    })


def new_agent(request):
    if request.method == 'POST':

        form = AgentForm(request.POST)

        if form.is_valid():
            data_form = form.cleaned_data

            cf = data_form.get('cf')
            name = data_form.get('name')
            surnames = data_form.get('surnames')
            category = data_form.get('category')
            residence = data_form.get('residence')

            agnt = Agent(
                cf=cf,
                name=name,
                surnames=surnames,
                category_id=category.id,
                residence_id=residence.id
            )

            agnt.save()

            # Crea mensaje flash
            messages.success(request, f'El agente {cf} se ha creado correctamente')

            return redirect('agents')
    else:
        form = AgentForm()

    return render(request, 'weekly/new-agent.html', {
        'title': 'Nuevo agente desde form',
        'form': form,
    })


def upload_doc(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            new_file_name = handle_uploaded_file(request.FILES['document'])

            excel_doc = Document()
            excel_doc.document = new_file_name
            excel_doc.save()

            messages.success(request, f'El archivo {new_file_name} se ha guardado correctamente')

            save_week_shifts(os.path.join(settings.MEDIA_ROOT, new_file_name))

            return redirect('upload_doc')

    else:
        form = DocumentForm()

    return render(request, 'weekly/upload-doc.html', {
        'title': 'Guardar archivo excel',
        'form': form
    })


def handle_uploaded_file(f):
    path_file = os.path.join(settings.MEDIA_ROOT, 'GSEM.xlsx')

    with open(path_file, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    new_name = rename_doc(path_file)
    shutil.move(new_name, f'media/{new_name}')

    return new_name
