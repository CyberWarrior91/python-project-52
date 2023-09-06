from django.test import TestCase, Client
from django.core.management import call_command
from django.urls import reverse
from django.utils.translation import activate


class UserAuthorizationCase(TestCase):
    fixtures = [
        'fixtures/userdata.json',
    ]

    def setUp(self):
        # Load fixtures
        call_command('loaddata', *self.fixtures)
        self.client = Client()
        self.login_url = reverse('login')
        self.home_page = '/ru/'

    def test_login(self):
        activate('ru')
        response = self.client.post(
            self.login_url,
            {'username': 'Mary', 'password': '12345ebat'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.home_page)

    def test_logout(self):
        self.client.login(username='Mary', password='12345ebat')
        response = self.client.get('/logout/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.home_page)
