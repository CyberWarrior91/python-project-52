from django.test import TestCase, Client
from .models import Task
from django.core.management import call_command
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from tests.test_crud_classes import ObjectCRUDCase
from tests.test_form_classes import ObjectFormTest
from django.urls import reverse_lazy
from .forms import TaskCreateForm
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
    index_page = 'task_index'
    objects_plural = 'tasks'
    template_name = 'tasks/index.html'

    def setUp(self):
        # Load fixtures
        call_command('loaddata', *self.fixtures)
        self.client = Client()

    def test_query_params(self):
        """
        Testing filter for tasks
        """
        test_user = User.objects.get(username='Mary')
        self.client.force_login(test_user)
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
        task = self.model.objects.create(
            name='first_task',
            description='test desc',
            creator=User.objects.get(first_name='Mary'),
            status=Status.objects.create(pk=99)
        )
        task.labels.add(Label.objects.get(pk=2), Label.objects.get(pk=3))
        task.save()
        self.assertTrue(
            self.model.objects.filter(
                name='first_task', description='test desc',
                creator='11', labels=(2, 3), status=99).exists()
        )

    def test_view_task(self):
        test_user = User.objects.get(username='Mary')
        self.client.force_login(test_user)
        task = self.model.objects.get(pk=2)
        response = self.client.get(reverse_lazy('task_single', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_single.html')
        response_object = response.context['task']
        self.assertEqual(response_object.name, task.name)


class CreateTaskFormCase(TestCase, ObjectFormTest):
    fixtures = ['fixtures/statusdata.json']
    form = TaskCreateForm
    correct_data = {
        'name': 'test task',
        'description': 'test description',
        'status': Status.objects.first(),
    }
    wrong_data = {
        'name': 'wrong task',
        'status': 'invalid status'
    }

    def setUp(self):
        # Load fixtures
        call_command('loaddata', *self.fixtures)
