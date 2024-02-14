from django.test import TestCase


class URLTests(TestCase):
    """
    Тест URL-адресов приложения, которые можно посетить. 
    Остальные используют редирект для GET-запросов и тестируются в test_views.py
    """
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_statistics(self):
        response = self.client.get('/stats/')
        self.assertEqual(response.status_code, 200)

    def test_admin(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
