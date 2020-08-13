from django.shortcuts import HttpResponse, render, redirect
from django.contrib import messages
from weekly.models import Agent, Residence, Category, Document
from weekly.forms import AgentForm, UploadDocumentForm


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
        agent = Agent.objects.get(pk=cf)
        response = f"Agente: {cf} {agent.name.title()} {agent.surnames.title()}"
    except:
        return render(request, 'weekly/weekly-agent.html', {
            'title': "Agente no encontrado", })
    return render(request, 'weekly/weekly-agent.html', {
        'title': 'Turnos del agente',
        'cf': agent.cf,
        'name': agent.name,
        'surnames': agent.surnames,
    })


def agents(request):
    # agents = Agent.objects.all()
    agents = Agent.objects.order_by('cf')

    return render(request, 'weekly/agents.html', {
        'title': 'Listado de agentes',
        'agents': agents,
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

            agent = Agent(
                cf=cf,
                name=name,
                surnames=surnames,
                category_id=category.id,
                residence_id=residence.id
            )

            agent.save()

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

        agent = Agent(
            cf=cf,
            name=name,
            surnames=surnames,
            category_id=category,
            residence_id=residence
        )

        agent.save()

        response = f"""
            <h2>Se ha creado el agente correctamente</h2>
            <strong>{agent.cf} {agent.name.title()} {agent.surnames.title()}, {category.name.title()}, {residence.name.title()}</strong>
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


def upload_doc(request):
    saved = False

    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)

        if form.is_valid():
            # TODO Cambiar nombre del fichero

            excel_doc = Document()
            excel_doc.name = form.cleaned_data['name']
            excel_doc.document = form.cleaned_data['excel_file']
            excel_doc.save()
            saved = True

            # Crea mensaje flash
            messages.success(request, f'El archivo {excel_doc.name} se ha guardado correctamente')

            return redirect('index')

    else:
        form = UploadDocumentForm()

    return render(request, 'weekly/upload-doc.html', {
        'title': 'Guardar archivo excel',
        'form': form,
        'saved': saved
    })

