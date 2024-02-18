import factory
import uuid
from django.test import TestCase
from main.models import Survey, Question, Choice, UsersActivity


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


class TestSurveyModel(TestCase):
    def setUp(self):
        self.survey = SurveyFactory(
            text="Sample Survey", description="Sample Survey Description"
        )

    def test_survey_text(self):
        self.assertEqual(self.survey.text, "Sample Survey")

    def test_survey_description(self):
        self.assertEqual(self.survey.description, "Sample Survey Description")

    def test_survey_str(self):
        self.assertEqual(str(self.survey), "Sample Survey")


class TestQuestionModel(TestCase):
    def setUp(self):
        self.question = QuestionFactory(
            text="Sample Question", description="Sample Question Description"
        )

    def test_question_text(self):
        self.assertEqual(self.question.text, "Sample Question")

    def test_question_description(self):
        self.assertEqual(self.question.description, "Sample Question Description")

    def test_question_str(self):
        self.assertEqual(str(self.question), "Sample Question")


class TestChoiceModel(TestCase):
    def setUp(self):
        self.choice = ChoiceFactory(text="Sample Choice")

    def test_choice_text(self):
        self.assertEqual(self.choice.text, "Sample Choice")

    def test_choice_str(self):
        self.assertEqual(str(self.choice), "Sample Choice")


class TestUsersActivityModel(TestCase):
    def setUp(self):
        self.user_activity = UsersActivityFactory(
            user_id="350c88bb5d9f449e9d4040e1e36dd496"
        )

    def test_user_activity_user_id(self):
        self.assertEqual(self.user_activity.user_id, "350c88bb5d9f449e9d4040e1e36dd496")

    def test_user_activity_str(self):
        self.assertEqual(str(self.user_activity), "350c88bb5d9f449e9d4040e1e36dd496")

    def test_user_activity_other(self):
        self.assertIsNotNone(self.user_activity.choice)
        self.assertIsNotNone(self.user_activity.question)
