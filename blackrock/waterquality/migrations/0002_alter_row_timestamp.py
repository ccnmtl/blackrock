# Generated by Django 3.2.23 on 2024-01-12 21:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('waterquality', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='row',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
