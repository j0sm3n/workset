import os, shutil
from django.shortcuts import HttpResponse, render, redirect
from django.contrib import messages
from django.conf import settings
from weekly.models import Agent, Residence, Category, Document
from weekly.forms import AgentForm, DocumentForm
from weekly.datos_excel import rename_doc


def index(request):

    documents = Document.objects.order_by('-document')

    return render(request, 'weekly/index.html', {
        'title': 'Gestión de turnos',
        'documents': documents,
    })


def weekly(request):

    document = Document.objects.latest('document')
    doc_path = os.path.join('media/documents', document.document.name)

    return render(request, 'weekly/weekly.html', {
        'title': 'Turnos semanales',
        'document': document,
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

            return redirect('upload_doc')

    else:
        form = DocumentForm()

    return render(request, 'weekly/upload-doc.html', {
        'title': 'Guardar archivo excel',
        'form': form
    })


# def handle_uploaded_file(f):
#     path_file = os.path.join(settings.MEDIA_ROOT, 'documents')
#     path_file = os.path.join(path_file, 'GSEM.xlsx')
#
#     with open(path_file, 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
#
#     new_name = rename_doc(path_file)
#     shutil.move(new_name, f'media/documents/{new_name}')
#
#     return new_name

def handle_uploaded_file(f):
    path_file = os.path.join(settings.MEDIA_ROOT, 'GSEM.xlsx')

    with open(path_file, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    new_name = rename_doc(path_file)
    shutil.move(new_name, f'media/{new_name}')

    return new_name
