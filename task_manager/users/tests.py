from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from django.contrib.messages import get_messages
# Create your tests here.


class UserTestCase(TestCase):

    fixtures = ['fixtures/userdata.json']

    def setUp(self):
        # Load fixtures
        call_command('loaddata', *self.fixtures)

    def test_create_user(self):
        user = User.objects.create(
            first_name='Ben',
            last_name='Green',
            username='Billy333',
            password='12345bill'
        )
        user.save()
        self.assertTrue(User.objects.filter(username='Billy333').exists())

    def test_change_user(self):
        user = User.objects.get(pk=1, username='Vlad')
        user.first_name = 'Bob'
        user.save()
        self.assertEqual(user.first_name, 'Bob')

    def test_change_user_failed(self):
        self.client.login(username='Mary', password='12345ebat')
        response = self.client.get('/en/users/2/update', follow=True)
        self.assertEqual(response.status_code, 200)
        # Check for flash message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have no rights to modify another user.')
        self.assertTemplateUsed(response, 'users/index.html')

    def test_delete_user(self):
        user = User.objects.get(username='Vlad')
        user.delete()
        self.assertRaises(User.DoesNotExist, User.objects.get, username='Vlad')
