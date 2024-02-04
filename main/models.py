from django.db import models


# Create your models here.
class Surveys(models.Model):
    survey_title = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Описание")

    def __str__(self) -> str:
        return self.survey_title


class Questions(models.Model):
    question_text = models.CharField(verbose_name="Вопрос", max_length=255)
    specifics = models.TextField(verbose_name="Подробности вопроса")
    survey = models.ForeignKey(Surveys, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.question_text


class Choices(models.Model):
    choice_text = models.CharField(verbose_name="Вариант ответа", max_length=255)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.choice_text


# TODO Do I need user here?
class Users(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=100)
    surname = models.CharField(verbose_name="Фамилия", max_length=100)

    def __str__(self) -> str:
        return self.name + " " + self.surname


class UsersActivity(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    # Do I need survey here? Because it already linked with question
    # survey = models.ForeignKey(surveys, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choices, on_delete=models.CASCADE)

    def __str__(self) -> str:
        # TODO What should I return here?
        return self.user.name  # This will not work
