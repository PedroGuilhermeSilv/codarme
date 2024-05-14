# Generated by Django 5.0.4 on 2024-05-01 20:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0002_agendamento_cancelado'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='prestador',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='agendamentos', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
