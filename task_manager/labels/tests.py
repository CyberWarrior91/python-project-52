from django.test import TestCase
from .models import Label
from django.core.management import call_command
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.utils.translation import activate
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.urls import reverse_lazy
# Create your tests here.


class LabelTestCase(TestCase):

    fixtures = [
        'fixtures/labeldata.json',
        'fixtures/userdata.json',
    ]

    def setUp(self):
        # Load fixtures
        call_command('loaddata', *self.fixtures)

    def test_create_label(self):
        label = Label.objects.create(name='test label')
        label.save()
        self.assertTrue(Label.objects.filter(name='test label').exists())

    def test_change_label(self):
        label = Label.objects.get(name='1 label')
        label.name = '1 test label'
        label.save()
        self.assertEqual(label.name, '1 test label')

    def test_delete_label(self):
        label = Label.objects.get(name='2 label')
        label.delete()
        self.assertRaises(Label.DoesNotExist, Label.objects.get, name='2 label')

    def test_delete_label_failed(self):
        activate('en')
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        label = Label.objects.get(pk=2)
        test_task = Task.objects.create(
            name='test',
            creator=user,
            status=Status.objects.create(name='test status'),
        )
        test_task.labels.add(label)
        response = self.client.post(
            reverse_lazy('label_delete',
                         kwargs={'pk': 2}),
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('label_index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Cannot delete the label, because it's being used"
        )
