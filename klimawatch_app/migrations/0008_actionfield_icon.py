# Generated by Django 5.0.4 on 2024-06-30 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('klimawatch_app', '0007_action_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionfield',
            name='icon',
            field=models.CharField(default='fa-suitcase', max_length=200),
        ),
    ]
