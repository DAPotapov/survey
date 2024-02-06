# Generated by Django 5.0.1 on 2024-02-05 15:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_rename_choices_choice_rename_questions_question_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="choice",
            options={
                "verbose_name": "Вариант ответа",
                "verbose_name_plural": "Варианты ответов",
            },
        ),
        migrations.AlterModelOptions(
            name="question",
            options={"verbose_name": "Вопрос", "verbose_name_plural": "Вопросы"},
        ),
        migrations.AlterModelOptions(
            name="survey",
            options={"verbose_name": "Опрос", "verbose_name_plural": "Опросы"},
        ),
        migrations.AlterField(
            model_name="question",
            name="specifics",
            field=models.TextField(blank=True, verbose_name="Подробности вопроса"),
        ),
        migrations.AlterField(
            model_name="survey",
            name="description",
            field=models.TextField(blank=True, verbose_name="Описание"),
        ),
    ]