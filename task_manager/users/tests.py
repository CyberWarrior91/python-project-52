from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from django.contrib.messages import get_messages
from django.utils.translation import activate
from django.urls import reverse_lazy
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
# Create your tests here.


class UserTestCase(TestCase):

    fixtures = [
        'fixtures/userdata.json',
        'fixtures/statusdata.json',
    ]
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
        response = self.client.get('/en/users/2/delete', follow=True)
        self.assertEqual(response.status_code, 200)
        delete_messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(delete_messages[0]), self.wrong_user_message)
        self.assertTemplateUsed(response, self.users_page)

    def test_delete_user_with_tasks_failed(self):
        activate('en')
        user = User.objects.get(username='Mary')
        task = Task.objects.create(
            name='test', 
            status=Status.objects.get(pk=3), 
            creator=user, 
            executor=user
        )
        user.task_set.add(task)
        self.client.force_login(user)
        # Get the delete URL for the user with their primary key
        # Send POST request to delete the user
        response = self.client.post(
            reverse_lazy('user_delete',
            kwargs={'pk': 1}), follow=True
        )
        # Check if the user is redirected back to the '/en/users/' page
        self.assertRedirects(response, reverse_lazy('users_index'))
        # Check if the error message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Unable to delete the user, because it's being used")
