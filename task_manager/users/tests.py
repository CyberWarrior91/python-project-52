from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from django.contrib.messages import get_messages
# Create your tests here.


class UserTestCase(TestCase):

    fixtures = ['fixtures/userdata.json']
    wrong_user_message = 'You have no rights to modify another user.'
    users_page = 'users/index.html'

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
        response_change = self.client.get('/en/users/2/update', follow=True)
        self.assertEqual(response_change.status_code, 200)
        change_messages = list(get_messages(response_change.wsgi_request))
        self.assertEqual(len(change_messages), 1)
        self.assertEqual(str(change_messages[0]), self.wrong_user_message)
        self.assertTemplateUsed(response_change, self.users_page)

    def test_delete_user(self):
        user = User.objects.get(username='Vlad')
        user.delete()
        self.assertRaises(User.DoesNotExist, User.objects.get, username='Vlad')

    def test_delete_user_failed(self):
        self.client.login(username='Mary', password='12345ebat')
        response_delete = self.client.get('/en/users/2/delete', follow=True)
        self.assertEqual(response_delete.status_code, 200)
        delete_messages = list(get_messages(response_delete.wsgi_request))
        self.assertEqual(str(delete_messages[0]), self.wrong_user_message)
        self.assertTemplateUsed(response_delete, self.users_page)

    def q_test_delete_user_with_tasks_failed(self):
        self.client.login(username='Mary', password='12345ebat')
        response = self.client.post('/en/users/1/delete', follow=True)
        self.assertEqual(response.status_code, 200)
        # Check if the error message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Unable to delete the user, because it's being used"
        )
        # Check if the user is redirected back to the '/en/users/' page
        self.assertRedirects(response, '/en/users/')
