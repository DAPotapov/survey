from django.test import TestCase
from main.models import Survey, Question, Choice, UsersActivity


class TestModels(TestCase):
    def test_survey(self):
        survey = Survey.objects.create(text="Test survey")
        self.assertEqual(survey.text, "Test survey")
