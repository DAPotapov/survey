from django.db import models


# Create your models here.
class surveys(models.Model):
    survey = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Описание")

    def __str__(self) -> str:
        return self.survey


class questions(models.Model):
    question = models.CharField(verbose_name="Вопрос", max_length=255)
    specifics = models.TextField(verbose_name="Подробности вопроса")
    survey = models.ForeignKey(surveys, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.question


class choices(models.Model):
    choice = models.CharField(verbose_name="Вариант ответа", max_length=255)
    question = models.ForeignKey(questions, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.choice


class users(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=100)
    surname = models.CharField(verbose_name="Фамилия", max_length=100)

    def __str__(self) -> str:
        return self.name + " " + self.surname


class user_activity(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    # Do I need survey here? Because it already linked with question
    # survey = models.ForeignKey(surveys, on_delete=models.CASCADE)
    question = models.ForeignKey(questions, on_delete=models.CASCADE)
    choice = models.ForeignKey(choices, on_delete=models.CASCADE)

    def __str__(self) -> str:
        # TODO What should I return here?
        return self.user.name
