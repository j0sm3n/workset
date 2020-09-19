from django.db import models


class Residence(models.Model):
    residence = models.CharField(max_length=20, verbose_name='Residencia')

    class Meta:
        verbose_name = 'residencia'
        verbose_name_plural = 'residencias'

    def __str__(self):
        return self.residence.title()


class Category(models.Model):
    category = models.CharField(max_length=20, verbose_name='Categoría')

    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'

    def __str__(self):
        return self.category.title()


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
    start = models.TimeField(verbose_name='Inicio', null=True, blank=True)
    end = models.TimeField(verbose_name='Fin', null=True, blank=True)
    category = models.CharField(max_length=20, verbose_name='Categoría', null=True, blank=True)

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


class Calendar(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.DO_NOTHING, verbose_name="Agente")
    calendar = models.CharField(max_length=100, unique=True, verbose_name='Calendario')

    class Meta:
        verbose_name = 'calendario'
        verbose_name_plural = 'calendarios'