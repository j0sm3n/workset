from django.db import models

from weekly.datos_excel import str_doc_date


class Residence(models.Model):
    name = models.CharField(max_length=20, verbose_name='Residencia')

    class Meta:
        verbose_name = 'residencia'
        verbose_name_plural = 'residencias'

    def __str__(self):
        return self.name.title()


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='Categoría')

    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'

    def __str__(self):
        return self.name.title()


class Agent(models.Model):
    cf = models.IntegerField(unique=True, primary_key=True, verbose_name='C.F.')
    name = models.CharField(max_length=50, verbose_name='Nombre')
    surnames = models.CharField(max_length=100, verbose_name='Apellidos')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='Categoría')
    residence = models.ForeignKey(Residence, on_delete=models.DO_NOTHING, verbose_name="Residencia")

    class Meta:
        verbose_name = 'agente'
        verbose_name_plural = 'agentes'
        ordering = ['name']

    def __str__(self):
        return f"{self.cf} {self.name.title()} {self.surnames.title()}"


class Shift(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name='Turno')
    start = models.TimeField(verbose_name='Inicio')
    end = models.TimeField(verbose_name='Fin')
    category = models.CharField(max_length=20, verbose_name='Categoría')

    class Meta:
        verbose_name = 'turno'
        verbose_name_plural = 'turnos'
        ordering = ['name']

    def __str__(self):
        return self.name


class AgentShift(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.DO_NOTHING, verbose_name='Turno')
    agent = models.ForeignKey(Agent, on_delete=models.DO_NOTHING, verbose_name='Agente')
    shift_date = models.DateField(verbose_name='Fecha')
    modified = models.BooleanField(verbose_name='Modificado')

    class Meta:
        verbose_name = 'turno agente'
        verbose_name_plural = 'turnos agente'
        ordering = ['agent', 'shift_date']

    def __str__(self):
        return f"{self.shift_date} {self.agent} {self.shift}"


class Document(models.Model):
    document = models.FileField(upload_to='documents/', verbose_name='Archivo excel')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Subido el')

    class Meta:
        verbose_name = 'documento'
        verbose_name_plural = 'documentos'
