from django.test import TestCase, Client
from django.core.management import call_command
from django.urls import reverse, reverse_lazy
from django.utils.translation import activate


class UserAuthorizationCase(TestCase):
    fixtures = [
        'fixtures/userdata.json',
    ]
    home_template_name = 'index.html'
    login_template_name = 'login.html'

    def setUp(self):
        # Load fixtures
        call_command('loaddata', *self.fixtures)
        self.client = Client()
        self.login_url = reverse('login')
        self.home_page = reverse_lazy('main')

    def test_login_success(self):
        activate('en')
        response = self.client.post(
            self.login_url,
            {'username': 'Mary', 'password': '12345ebat'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.home_page)
        self.assertTemplateUsed(response, self.home_template_name)

    def test_login_failed(self):
        activate('ru')
        response = self.client.post(
            self.login_url,
            {'username': 'Mary', 'password': 'wrongpass'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.login_template_name)

    def test_logout(self):
        self.client.login(username='Mary', password='12345ebat')
        response = self.client.get('/logout/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.home_page)
        self.assertTemplateUsed(response, self.home_template_name)

    def test_homepage(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.home_template_name)
