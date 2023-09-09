from django.test import TestCase, Client
from .models import Task
from django.core.management import call_command
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from tests.test_crud_classes import ObjectCRUDCase
# Create your tests here.


class TaskTestCase(TestCase, ObjectCRUDCase):

    fixtures = [
        'fixtures/taskdata.json',
        'fixtures/labeldata.json',
        'fixtures/userdata.json',
        'fixtures/statusdata.json'
    ]
    pk = 2
    model = Task

    def setUp(self):
        # Load fixtures
        call_command('loaddata', *self.fixtures)
        self.client = Client()

    def test_query_params(self):
        """
        Testing filter for tasks
        """
        test_user = User.objects.get(username='Mary')
        self.client.login(username=test_user.username, password='12345ebat')
        response = self.client.get(
            '/en/tasks/',
            {
                'status': 1,
                'executor': 5,
                'labels': 2,
                'show_my_tasks': True
            }
        )
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 2)

    def test_create_object(self):
        task = Task.objects.create(
            name='first_task',
            description='test desc',
            creator=User.objects.get(first_name='Mary'),
            status=Status.objects.create(pk=99)
        )
        task.labels.add(Label.objects.get(pk=2), Label.objects.get(pk=3))
        task.save()
        self.assertTrue(
            Task.objects.filter(
                name='first_task', description='test desc',
                creator='11', labels=(2, 3), status=99).exists()
        )
