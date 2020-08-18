from django import forms
from django.forms import ModelForm
from django.core import validators

from .models import Category, Residence, Document


class AgentForm(forms.Form):
    cf = forms.CharField(label='C.F.', min_length=3, max_length=4, required=True, validators=[
        validators.RegexValidator('[0-9]{3,4}', 'El C.F. sólo puede contener números')])
    name = forms.CharField(label='Nombre', required=True, validators=[
        validators.MinLengthValidator(3, 'El nombre es muy corto')])
    surnames = forms.CharField(label='Apellidos', required=True, validators=[
        validators.MinLengthValidator(3, 'Los apellidos son muy cortos')])
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Categoría')
    residence = forms.ModelChoiceField(queryset=Residence.objects.all(), label='Residencia')

    cf.widget.attrs.update({
        'placeholder': 'Carné ferroviario',
        'class': 'cf_content_form'
    })
    name.widget.attrs.update({
        'placeholder': 'Nombre del agente',
        'class': 'name_content_form'
    })
    surnames.widget.attrs.update({
        'placeholder': 'Apellidos del agente',
        'class': 'surnames_content_form'
    })


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['document', ]
