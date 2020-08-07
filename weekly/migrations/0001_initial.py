# Generated by Django 3.0.3 on 2020-08-06 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agents',
            fields=[
                ('cf', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('surnames', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=20)),
                ('residence', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Shifts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True)),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('category', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='AgentShifts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift_date', models.DateField()),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='weekly.Agents')),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='weekly.Shifts')),
            ],
        ),
    ]