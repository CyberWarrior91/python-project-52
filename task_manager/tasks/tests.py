from django.test import TestCase, Client
from .models import Task
from django.core.management import call_command
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

# Create your tests here.

class UserTestCase(TestCase):
    
    fixtures = [
        'fixtures/taskdata.json', 
        'fixtures/labeldata.json', 
        'fixtures/userdata.json', 
        'fixtures/statusdata.json'
        ]

    def setUp(self):
        # Load fixtures
        call_command('loaddata', *self.fixtures)
        self.client = Client()

    def test_query_params(self):
        test_user = User.objects.get(username='Mary')
        self.client.login(username=test_user.username, password='12345ebat')
        response = self.client.get('/en/tasks/', {'status': 1, 'executor': 5, 'labels': 2})
        tasks = response.context['tasks']  # Assuming the context variable is named 'tasks'
        # Assert that there are exactly 2 tasks in the response
        self.assertEqual(len(tasks), 2)


    def test_create_task(self):
        task = Task.objects.create(
            name='first_task', description='test desc', creator=User.objects.get(first_name='Mary'),
            status=Status.objects.create(pk=99))
        task.labels.add(Label.objects.get(pk=2), Label.objects.get(pk=3))
        task.save()
        self.assertTrue(
            Task.objects.filter(
            name='first_task', description='test desc',
            creator='11',  labels=(2, 3), status=99).exists()
            )

    def test_change_task(self):
        task = Task.objects.get(pk=2)
        task.name = 'second task'
        task.save()
        self.assertEqual(task.name, 'second task')

    def test_delete_task(self):
        task = Task.objects.get(pk=2)
        task.delete()
        self.assertRaises(Task.DoesNotExist, Task.objects.get, pk=2)
