import factory
import uuid
from .models import Survey, Question, Choice, UsersActivity


class SurveyFactory(factory.Factory):
    class Meta:
        model = Survey

    text = factory.Faker("sentence")
    description = factory.Faker("sentence")

    # Save the survey in the database
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        survey = super()._create(model_class, *args, **kwargs)
        survey.save()
        return survey


class QuestionFactory(factory.Factory):
    class Meta:
        model = Question

    text = factory.Faker("sentence")
    description = factory.Faker("sentence")
    survey = factory.SubFactory(SurveyFactory)

    # Save the question in the database
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        question = super()._create(model_class, *args, **kwargs)
        question.save()
        return question


class ChoiceFactory(factory.Factory):
    class Meta:
        model = Choice

    text = factory.Faker("sentence")
    question = factory.SubFactory(QuestionFactory)
    next_question = factory.SubFactory(QuestionFactory)

    # Save the choice in the database
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        choice = super()._create(model_class, *args, **kwargs)
        choice.save()
        return choice
    

class UsersActivityFactory(factory.Factory):
    class Meta:
        model = UsersActivity

    user_id = uuid.uuid4().hex
    choice = factory.SubFactory(ChoiceFactory)
    question = factory.SubFactory(QuestionFactory)

    # Save the user activity in the database
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user_activity = super()._create(model_class, *args, **kwargs)
        user_activity.save()
        return user_activity
