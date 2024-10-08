# Generated by Django 5.1.1 on 2024-09-08 14:38

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plugin',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('schema', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='ServerPlugins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=16, null=True)),
                ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.plugin')),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.server')),
            ],
        ),
        migrations.AddField(
            model_name='server',
            name='plugins',
            field=models.ManyToManyField(related_name='servers', through='api.ServerPlugins', to='api.plugin'),
        ),
    ]
