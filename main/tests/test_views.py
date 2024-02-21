import re
import pprint
from django.test import TestCase, Client
from django.urls import reverse
from main.views import index, treat_survey, treat_answer, statistics, get_results_orm
from main.models import Survey, Question, Choice, UsersActivity
from main.factories import SurveyFactory, QuestionFactory, ChoiceFactory, UsersActivityFactory


class TestIndexView(TestCase):
    def setUp(self):
        self.client = Client()
        self.survey_factory = SurveyFactory()

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
    def setUp(self):
        self.client = Client()
        self.activities = UsersActivityFactory.create_batch(3)

    def test_statistics_open(self):
        response = self.client.get(reverse("stats"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/statistics.html")

    def test_statistics_content(self):
        response = self.client.get(reverse("stats"))
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context["stats"]), 0)

    def test_statistics_empty(self):
        Survey.objects.all().delete()
        response = self.client.get(reverse("stats"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/error.html")
        self.assertQuerySetEqual(response.context["error"], 'Надо же... ни одного опроса нет ещё...')

class TestGetResults(TestCase):
    def setUp(self):
        self.client = Client()
        self.activities = UsersActivityFactory.create_batch(10)

    def test_get_results(self):
        # TODO фабрики надо переделать, один-ко-многим было реально 1 ко многим. Иначе сложно тестировать, когда 1 ответ на 1 вопрос в 1 опросе. И то не всегда.
        print(get_results_orm(3))
