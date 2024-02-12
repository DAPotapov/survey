from django.test import TestCase
from main.views import index, treat_survey, treat_answer, statistics


class TestViews(TestCase):
    def test_index(self):
        response = index(self)
        self.assertEqual(response.status_code, 200)

    def test_statistics(self):
        response = statistics(self)
        self.assertEqual(response.status_code, 200)
