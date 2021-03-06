# Generated by Django 3.0.3 on 2020-09-18 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weekly', '0010_auto_20200907_1257'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calendar_id', models.CharField(max_length=100, unique=True, verbose_name='Calendario')),
                ('agent_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='weekly.Agent', verbose_name='Agente')),
            ],
            options={
                'verbose_name': 'calendario',
                'verbose_name_plural': 'calendarios',
            },
        ),
    ]
