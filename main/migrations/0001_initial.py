# Generated by Django 5.0.1 on 2024-02-04 08:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="questions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question", models.CharField(max_length=255, verbose_name="Вопрос")),
                ("specifics", models.TextField(verbose_name="Подробности вопроса")),
            ],
        ),
        migrations.CreateModel(
            name="surveys",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("survey", models.CharField(max_length=100, verbose_name="Название")),
                ("description", models.TextField(verbose_name="Описание")),
            ],
        ),
        migrations.CreateModel(
            name="users",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Имя")),
                ("surname", models.CharField(max_length=100, verbose_name="Фамилия")),
            ],
        ),
        migrations.CreateModel(
            name="choices",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "choice",
                    models.CharField(max_length=255, verbose_name="Вариант ответа"),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.questions"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="questions",
            name="survey",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="main.surveys"
            ),
        ),
        migrations.CreateModel(
            name="user_activity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "choice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.choices"
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.questions"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.users"
                    ),
                ),
            ],
        ),
    ]