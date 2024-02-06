# Generated by Django 5.0.1 on 2024-02-06 13:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0007_choice_next_question_alter_choice_question"),
    ]

    operations = [
        migrations.AlterField(
            model_name="choice",
            name="next_question",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lead_choices",
                to="main.question",
            ),
        ),
    ]
