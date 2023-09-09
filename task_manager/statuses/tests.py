from django.test import TestCase, Client
from .models import Status
from django.contrib.auth.models import User
from task_manager.tasks.models import Task
from django.core.management import call_command
from django.urls import reverse_lazy
from django.contrib.messages import get_messages
from django.utils.translation import activate
# Create your tests here.


class StatusTestCase(TestCase):

    fixtures = [
        'fixtures/statusdata.json',
        'fixtures/userdata.json',
    ]

    def setUp(self):
        # Load fixtures
        call_command('loaddata', *self.fixtures)
        self.client = Client()

    def test_create_status(self):
        status = Status.objects.create(name='zero status')
        status.save()
        self.assertTrue(Status.objects.filter(name='zero status').exists())

    def test_change_status(self):
        status = Status.objects.get(name='new')
        status.name = 'test new'
        status.save()
        self.assertEqual(status.name, 'test new')

    def test_delete_status(self):
        status = Status.objects.get(name='done')
        status.delete()
        self.assertRaises(Status.DoesNotExist, Status.objects.get, name='done')

    def test_delete_status_failed(self):
        activate('en')
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        status = Status.objects.get(pk=1)
        Task.objects.create(name='test', creator=user, status=status)
        response = self.client.post(
            reverse_lazy('status_delete',
                         kwargs={'pk': 1}),
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('status_index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Cannot delete the status, because it's being used"
        )
