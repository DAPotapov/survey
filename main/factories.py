import factory
import uuid
from .models import Survey, Question, Choice, UsersActivity


class SurveyFactory(factory.django.DjangoModelFactory):
    """
    Создаёт произвольный опрос с двумя связанными вопросами (по умолчанию).
    Если это не требуется, то при вызове надо указать questions=None
    """

    class Meta:
        model = Survey

    text = factory.Faker("sentence")
    description = factory.Faker("sentence")
    # Создаем 2 связанных вопроса
    questions = factory.RelatedFactoryList(
        "main.factories.QuestionFactory",
        factory_related_name="survey",
        size=2,
    )
    first_question = None


class QuestionFactory(factory.django.DjangoModelFactory):
    """
    Создаёт произвольный вопрос с двумя связанными вариантами ответа (по умолчанию).
    Вопрос привязывается к первому попавшемуся опросу (или создаётся новый).
    Если это не требуется, то при вызове надо указать choices=None
    """

    class Meta:
        model = Question

    text = factory.Faker("sentence")
    description = factory.Faker("sentence")

    # Аналогично создаём связанные варианты ответов
    choices = factory.RelatedFactoryList(
        "main.factories.ChoiceFactory", factory_related_name="question", size=2
    )

    # Привязываем вопрос к существующему опросу, или создаём новый
    @factory.lazy_attribute
    def survey(self):
        try:
            return next(Survey.objects.iterator())
        except StopIteration:
            return SurveyFactory.create(questions=None)

    # TODO first_question должен быть именно этот, если опрос создан из вопроса. Попробовать post_generation


class ChoiceFactory(factory.django.DjangoModelFactory):
    """
    Создаёт новый вариант ответа, который привязывается
    к первому попавшемуся вопросу или создаёт новый.
    """

    class Meta:
        model = Choice

    text = factory.Faker("sentence")

    # Связываем вариант ответа с существующим вопросом,
    # но во избежание рекурсии подавляем запуск RelatedFactoryList
    @factory.lazy_attribute
    def question(self):
        try:
            return next(Question.objects.iterator())
        except StopIteration:
            return QuestionFactory.create(choices=None)

    # По умолчанию, следующий вопрос не задан.
    # При создании дерева опроса надо будет его указать.
    next_question = None


class UsersActivityFactory(factory.django.DjangoModelFactory):
    """
    Создаёт новую запись о выборе пользователя.
    TODO надо чтобы при вызове из batch создавались разные записи
    (сейчас дублируется одна и та же)
    """

    class Meta:
        model = UsersActivity

    user_id = uuid.uuid4().hex

    @factory.lazy_attribute
    def choice(self):
        try:
            return next(Choice.objects.iterator())
        except StopIteration:
            return ChoiceFactory.create(question=None)

    question = factory.SelfAttribute("choice.question")
