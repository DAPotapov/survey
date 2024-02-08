from email.policy import default
import uuid
from django.db import models


# Create your models here.
class Survey(models.Model):
    text = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self) -> str:
        return self.text


class Question(models.Model):
    text = models.CharField(verbose_name="Вопрос", max_length=255)
    description = models.TextField(verbose_name="Подробности вопроса", blank=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    # TODO Нужно для определения первого вопроса. Ещё для чего?
    # Лучше заменить булевым полем и сделать функцию проверки, что 1 вопрос - один
    # Сейчас дублирует иерархию, определяемую вариантами ответов и может противоречить ей
    parent_question = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self) -> str:
        return self.text


class Choice(models.Model):
    text = models.CharField(verbose_name="Вариант ответа", max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    # Здесь умышленно иду по пути нормализации БД в ущерб производительности,
    # Исходя из принципа "простое - лучше сложного"
    # survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    next_question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, related_name="lead_choices", default=None, null=True)

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self) -> str:
        return self.text


class UsersActivity(models.Model):
    user_id = models.CharField(max_length=40)
    # Do I need survey here? Because it already linked with question
    # survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Активность пользователя"
        verbose_name_plural = "Активность пользователей"

    def __str__(self) -> str:
        # TODO What should I return here?
        return str(self.user_id)  # This will not work
