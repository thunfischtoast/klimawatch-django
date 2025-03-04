# Generated by Django 5.0.4 on 2024-04-14 11:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('klimawatch_app', '0002_markdowncontent'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmissionData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emissions', models.JSONField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('kommune', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='klimawatch_app.kommune')),
            ],
        ),
    ]
