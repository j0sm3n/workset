# Generated by Django 3.0.3 on 2020-09-18 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weekly', '0011_calendar'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='modified',
            field=models.BooleanField(default=True),
        ),
    ]
