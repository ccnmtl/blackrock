# Generated by Django 3.2.23 on 2024-01-11 20:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_auto_20220408_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_date'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='modified_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='modified_date'),
        ),
        migrations.AlterField(
            model_name='digitalobject',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_date'),
        ),
        migrations.AlterField(
            model_name='digitalobject',
            name='modified_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='modified_date'),
        ),
        migrations.AlterField(
            model_name='foreststory',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_date'),
        ),
        migrations.AlterField(
            model_name='foreststory',
            name='modified_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='modified_date'),
        ),
        migrations.AlterField(
            model_name='learningactivity',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_date'),
        ),
        migrations.AlterField(
            model_name='learningactivity',
            name='modified_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='modified_date'),
        ),
        migrations.AlterField(
            model_name='location',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_date'),
        ),
        migrations.AlterField(
            model_name='location',
            name='modified_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='modified_date'),
        ),
        migrations.AlterField(
            model_name='person',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_date'),
        ),
        migrations.AlterField(
            model_name='person',
            name='modified_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='modified_date'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_date'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='modified_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='modified_date'),
        ),
        migrations.AlterField(
            model_name='region',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_date'),
        ),
        migrations.AlterField(
            model_name='region',
            name='modified_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='modified_date'),
        ),
        migrations.AlterField(
            model_name='researchproject',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_date'),
        ),
        migrations.AlterField(
            model_name='researchproject',
            name='modified_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='modified_date'),
        ),
        migrations.AlterField(
            model_name='station',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_date'),
        ),
        migrations.AlterField(
            model_name='station',
            name='modified_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='modified_date'),
        ),
    ]
