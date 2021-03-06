# Generated by Django 3.0.3 on 2020-09-19 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weekly', '0015_auto_20200918_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='category',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Categoría'),
        ),
        migrations.AlterField(
            model_name='shift',
            name='end',
            field=models.TimeField(blank=True, null=True, verbose_name='Fin'),
        ),
        migrations.AlterField(
            model_name='shift',
            name='start',
            field=models.TimeField(blank=True, null=True, verbose_name='Inicio'),
        ),
    ]
