import factory
import uuid
from .models import Survey, Question, Choice, UsersActivity


class SurveyFactory(factory.Factory):
    class Meta:
        model = Survey

    text = factory.Faker("sentence")
    description = factory.Faker("sentence")


class QuestionFactory(factory.Factory):
    class Meta:
        model = Question

    text = factory.Faker("sentence")
    description = factory.Faker("sentence")
    survey = factory.SubFactory(SurveyFactory)


class ChoiceFactory(factory.Factory):
    class Meta:
        model = Choice

    text = factory.Faker("sentence")
    question = factory.SubFactory(QuestionFactory)
    next_question = factory.SubFactory(QuestionFactory)


class UsersActivityFactory(factory.Factory):
    class Meta:
        model = UsersActivity

    user_id = uuid.uuid4().hex
    choice = factory.SubFactory(ChoiceFactory)
    question = factory.SubFactory(QuestionFactory)
