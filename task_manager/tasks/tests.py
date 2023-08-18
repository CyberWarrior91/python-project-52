from django.test import TestCase
from .models import Task
from django.core.management import call_command
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.tags.models import Tag
# Create your tests here.

class UserTestCase(TestCase):
    
    fixtures = ['fixtures/taskdata.json', 'fixtures/tagdata.json', 'fixtures/userdata.json', 'fixtures/statusdata.json']

    def setUp(self):
        # Load fixtures
        call_command('loaddata', *self.fixtures)

    def test_create_task(self):
        task = Task.objects.create(
            name='first_task', description='test desc', creator=User.objects.get(first_name='Mary'),
            status=Status.objects.create(pk=99))
        task.tags.add(Tag.objects.create(pk=1), Tag.objects.create(pk=2))
        task.save()
        self.assertTrue(
            Task.objects.filter(
            name='first_task', description='test desc',
            creator='11',  tags=(1, 2), status=99).exists()
            )

    def test_change_task(self):
        task = Task.objects.get(pk=1)
        task.name = 'second task'
        task.save()
        self.assertEqual(task.name, 'second task')

    def test_delete_task(self):
        task = Task.objects.get(pk=1)
        task.delete()
        self.assertRaises(Task.DoesNotExist, Task.objects.get, pk=1)
