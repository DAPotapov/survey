from django.test import TestCase
from main.views import index, treat_survey, treat_answer, statistics
from main.models import Survey, Question, Choice, UsersActivity


class TestIndexView(TestCase):
    def test_index(self):
        response = index(self)
        self.assertEqual(response.status_code, 200)

    def test_no_surveys(self):
        Survey.objects.all().delete()        
        response = index(self)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["surveys"], [])


class TestStatisticsView(TestCase):
    def test_statistics(self):
        response = statistics(self)
        self.assertEqual(response.status_code, 200)
