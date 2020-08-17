import os, shutil
from django.shortcuts import HttpResponse, render, redirect
from django.contrib import messages
from django.conf import settings
from weekly.models import Agent, Residence, Category, Document
from weekly.forms import AgentForm, DocumentForm
from weekly.datos_excel import rename_doc


def index(request):
    return render(request, 'weekly/index.html', {
        'title': 'Gestión de turnos',
    })


def weekly(request):
    return render(request, 'weekly/weekly.html', {
        'title': 'Turnos semanales',
    })


def weekly_agent(request):
    return render(request, 'weekly/weekly-agent.html', {
        'title': 'Turnos del agente'
    })


# def new_agent(request, cf, name, surnames, category, residence):
#     agent = Agent(
#         cf = cf,
#         name = name,
#         surnames = surnames,
#         category = category,
#         residence = residence
#     )
#     agent.save()
#
#     html = f"Creado el agente <strong>{agent.cf} \
#             {agent.name} {agent.surnames}</strong>"
#
#     return HttpResponse(html)

# def agent(request, cf):
#     try:
#         agent = Agent.objects.get(pk=cf)
#         response = f"Agente: {cf} {agent.name.title()} {agent.surnames.title()}"
#     except:
#         response = "<strong>Agente no encontrado</strong>"
#     return HttpResponse(response)

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
    # agents = Agent.objects.all()
    agnts = Agent.objects.order_by('cf')

    return render(request, 'weekly/agents.html', {
        'title': 'Listado de agentes',
        'agents': agnts,
    })


def new_agent(request):
    residences = Residence.objects.all()
    categories = Category.objects.all()

    return render(request, 'weekly/new-agent.html', {
        'title': 'Nuevo agente',
        'residences': residences,
        'categories': categories,
    })


def new_form_agent(request):
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

    return render(request, 'weekly/new-form-agent.html', {
        'title': 'Nuevo agente desde form',
        'form': form,
    })


def save_agent(request):
    if request.method == 'POST':

        cf = request.POST['cf']
        name = request.POST['name']
        surnames = request.POST['surnames']
        category = request.POST['category']
        residence = request.POST['residence']

        agnt = Agent(
            cf=cf,
            name=name,
            surnames=surnames,
            category_id=category,
            residence_id=residence
        )

        agnt.save()

        response = f"""
            <h2>Se ha creado el agente correctamente</h2>
            <strong>
                {agnt.cf} {agnt.name.title()} {agnt.surnames.title()}, {category.name.title()}, {residence.name.title()}
            </strong>
            <br>
            <a href="../new-agent/">Volver</a>
        """

    else:
        response = """
            <h2>No se ha podido crear el agente</h2>
            <br>
            <a href="../new-agent/">Volver</a>
        """

    return HttpResponse(response)


# def upload_doc(request):
#
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             # TODO Cambiar nombre del fichero
#             # ERROR: Busca en la carpeta documents para renombrar, pero como todavía
#             #        no se ha guardado el archivo salta un FileNotFoundError
#
#             excel_doc = Document()
#             # excel_doc.document = form.cleaned_data['document']
#             path = os.path.join(settings.MEDIA_ROOT, 'documents')
#             saved_doc = os.path.join(path, form.cleaned_data['document'].name)
#             new_file_name = str_doc_date(saved_doc)
#             new_file_name += "_SEM.xlsx"
#             excel_doc.document = new_file_name
#             excel_doc.save()
#
#             # rename_doc(saved_doc)
#
#             # Crea mensaje flash
#             messages.success(request, f'El archivo {new_file_name} se ha guardado correctamente')
#             # messages.success(request, type(excel_doc.document))
#
#             return redirect('index')
#
#     else:
#         form = DocumentForm()
#
#     return render(request, 'weekly/upload-doc.html', {
#         'title': 'Guardar archivo excel',
#         'form': form
#     })


def upload_doc(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            new_file_name = handle_uploaded_file(request.FILES['document'])

            excel_doc = Document()
            excel_doc.document = new_file_name
            excel_doc.save()

            messages.success(request, f'El archivo {new_file_name} se ha guardado correctamente')

            return redirect('index')

    else:
        form = DocumentForm()

    return render(request, 'weekly/upload-doc.html', {
        'title': 'Guardar archivo excel',
        'form': form
    })


def handle_uploaded_file(f):
    path_file = os.path.join(settings.MEDIA_ROOT, 'documents')
    path_file = os.path.join(path_file, 'GSEM.xlsx')

    with open(path_file, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    new_name = rename_doc(path_file)
    shutil.move(new_name, f'media/documents/{new_name}')

    return new_name
