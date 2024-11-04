# Generated by Django 5.1.2 on 2024-11-02 15:17

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('started_at', models.DateTimeField(null=True)),
                ('colour', models.CharField(choices=[('white', 'Белый'), ('black', 'Черный')], max_length=10)),
                ('finished_at', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('pending', 'Ожидание'), ('in_progress', 'В процессе'), ('finished', 'Завершено')], default='pending', max_length=30)),
                ('pgn', models.TextField()),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Games',
            },
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('number', models.IntegerField()),
                ('text', models.CharField(max_length=10)),
                ('fen', models.TextField()),
                ('source', models.CharField(choices=[('user', 'Пользователь'), ('bot', 'Бот')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.game')),
            ],
            options={
                'unique_together': {('game_id', 'number')},
            },
        ),
    ]