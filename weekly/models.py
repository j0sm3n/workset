from django.db import models

class Agent(models.Model):
    cf = models.IntegerField(unique=True, primary_key=True, verbose_name='C.F.')
    name = models.CharField(max_length=50, verbose_name='Nombre')
    surnames = models.CharField(max_length=100, verbose_name='Apellidos')
    category = models.CharField(max_length=20, verbose_name='Categoría')
    residence =models.CharField(max_length=20, verbose_name='Residencia')

    class Meta:
        verbose_name = 'agente'
        verbose_name_plural = 'agentes'
        ordering = ['surnames']

    def __str__(self):
        return self.name


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

    class Meta:
        verbose_name = 'turno_agente'
        verbose_name_plural = 'turnos_agente'
        ordering = ['agent', 'shift_date']

    def __str__(self):
        return f"{self.shift_date} {self.agent} {self.shift}"
