# Generated by Django 5.0.1 on 2024-02-04 10:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_rename_user_activity_usersactivity"),
    ]

    operations = [
        migrations.RenameField(
            model_name="choices",
            old_name="choice",
            new_name="choice_text",
        ),
        migrations.RenameField(
            model_name="questions",
            old_name="question",
            new_name="question_text",
        ),
        migrations.RenameField(
            model_name="surveys",
            old_name="survey",
            new_name="survey_title",
        ),
    ]