from django.test import Client
from django.test import RequestFactory, TestCase

class UrlTests(TestCase):
 
 def test_createBets(self):
  response = self.client.get('get/upcoming_games/Bundesliga/')
  print(response)
  self.assertEqual(200, response.status_code)
