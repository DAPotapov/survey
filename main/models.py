from django.db import models


class Survey(models.Model):
    """ Таблица с опросами """

    text = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self) -> str:
        return self.text


class Question(models.Model):
    """ Таблица с вопросами """

    text = models.CharField(verbose_name="Вопрос", max_length=255)
    description = models.TextField(verbose_name="Подробности вопроса", blank=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    parent_question = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self) -> str:
        return self.text


class Choice(models.Model):
    """ Таблица с вариантами ответов """

    text = models.CharField(verbose_name="Вариант ответа", max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    # Здесь умышленно иду по пути нормализации БД в ущерб производительности,
    # исходя из принципа "простое - лучше сложного"
    # survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    next_question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, related_name="lead_choices", default=None, null=True)

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self) -> str:
        return self.text


class UsersActivity(models.Model):
    """ Таблица, хранящая записи о данных пользователем ответах на вопросы """
    
    user_id = models.CharField(max_length=40)
    # В целях нормализации связь с survey через question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Активность пользователя"
        verbose_name_plural = "Активность пользователей"

    def __str__(self) -> str:
        return str(self.user_id)
