from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.management import call_command
from django.contrib.messages import get_messages
from django.utils.translation import activate
from django.urls import reverse_lazy
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from test_mixins.test_crud_classes import ObjectCRUDCase
from test_mixins.test_form_classes import ObjectFormTest
from .forms import UserCreationForm, UserUpdateForm
# Create your tests here.


class UserTestCase(TestCase, ObjectCRUDCase):

    fixtures = [
        'fixtures/userdata.json',
        'fixtures/statusdata.json',
    ]
    wrong_user_message = 'У вас нет прав для изменения другого пользователя.'
    index_page = 'users_index'
    model = User
    pk = 1
    objects_plural = 'users'
    template_name = 'users/index.html'

    def setUp(self):
        # Load fixtures
        call_command('loaddata', *self.fixtures)
        self.client = Client()

    def test_create_object(self):
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

    def test_users_list(self):
        url = reverse_lazy('users_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')
        users = response.context['users']
        for user in users:
            self.assertIsInstance(user, User)

    def test_change_other_user_failed(self):
        user = User.objects.get(username="Mary")
        self.client.force_login(user)
        """
        Testing whether the error message shows up and redirect happens
        when trying to change other user's data
        """
        response_change = self.client.get('/users/2/update', follow=True)
        self.assertEqual(response_change.status_code, 200)
        change_messages = list(get_messages(response_change.wsgi_request))
        self.assertEqual(len(change_messages), 1)
        self.assertEqual(str(change_messages[0]), self.wrong_user_message)
        self.assertTemplateUsed(response_change, self.template_name)
        """
        Testing the same behaviour for removal of other user
        """
        response_delete = self.client.get('/users/2/delete', follow=True)
        self.assertEqual(response_delete.status_code, 200)
        delete_messages = list(get_messages(response_delete.wsgi_request))
        self.assertEqual(str(delete_messages[0]), self.wrong_user_message)
        self.assertTemplateUsed(response_delete, self.template_name)

    def test_delete_user_with_tasks_failed(self):
        """
        Testing removal of a user who is linked with any tasks
        """
        activate('en')
        user = User.objects.get(username='Mary')
        task = Task.objects.create(
            name='test',
            status=Status.objects.get(pk=3),
            creator=user,
            executor=user,
        )
        user.executor.add(task)
        self.client.force_login(user)
        response = self.client.post(
            reverse_lazy('user_delete',
                         kwargs={'pk': 1}),
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('users_index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Невозможно удалить пользователя, потому что он используется"
        )


class CreateUserFormTestCase(TestCase, ObjectFormTest):
    form = UserCreationForm
    correct_data = {
        'first_name': 'test',
        'last_name': 'user',
        'username': 'test',
        'password1': 'testuser',
        'password2': 'testuser',
    }
    wrong_data = {
        'first_name': 'test',
        'last_name': 'user',
        'username': 'test',
        'password1': '123',
        'password2': '1234',
    }


class UpdateUserFormTestCase(TestCase, ObjectFormTest):
    form = UserUpdateForm
    correct_data = {
        'first_name': 'test',
        'last_name': 'user',
        'username': 'test',
        'password1': 'testuser1',
        'password2': 'testuser1',
    }
    wrong_data = {
        'username': 'test',
        'password1': 'test',
        'password2': 'testuser',
    }
