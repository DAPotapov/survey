import re
from django.test import TestCase, Client
from django.urls import reverse
from main.views import index, treat_survey, treat_answer, statistics
from main.models import Survey, Question, Choice, UsersActivity


class TestIndexView(TestCase):
    def setUp(self):
        self.client = Client()
        self.survey = Survey.objects.create(text="Sample Survey", description="Sample Survey description")

    def test_index(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")
        # Check that the survey list is not empty
        self.assertGreater(len(response.context["surveys"]), 0)

    def test_no_surveys(self):
        Survey.objects.all().delete()
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["surveys"], [])


class TestStatisticsView(TestCase):
    def test_statistics(self):
        response = statistics(self)
        self.assertEqual(response.status_code, 200)
