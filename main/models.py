from email.policy import default
import uuid
from django.db import models


# Create your models here.
class Survey(models.Model):
    survey_title = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self) -> str:
        return self.survey_title


class Question(models.Model):
    question_text = models.CharField(verbose_name="Вопрос", max_length=255)
    specifics = models.TextField(verbose_name="Подробности вопроса", blank=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    parent_question = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self) -> str:
        return self.question_text


class Choice(models.Model):
    choice_text = models.CharField(verbose_name="Вариант ответа", max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    # survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    next_question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, related_name="lead_choices", default=None, null=True)

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self) -> str:
        return self.choice_text


class UsersActivity(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    # Do I need survey here? Because it already linked with question
    # survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Активность пользователя"
        verbose_name_plural = "Активность пользователей"

    def __str__(self) -> str:
        # TODO What should I return here?
        return self.user.name  # This will not work
