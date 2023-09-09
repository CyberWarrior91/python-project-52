from django.test import TestCase, Client
from .models import Status
from django.contrib.auth.models import User
from task_manager.tasks.models import Task
from django.core.management import call_command
from django.urls import reverse_lazy
from django.contrib.messages import get_messages
from django.utils.translation import activate
from tests.test_crud_classes import ObjectCRUDCase
# Create your tests here.


class StatusTestCase(TestCase, ObjectCRUDCase):

    fixtures = [
        'fixtures/statusdata.json',
        'fixtures/userdata.json',
    ]
    model = Status
    pk = 5
    index_page = 'status_index'
    objects_plural = 'statuses'
    template_name = 'statuses/index.html'

    def setUp(self):
        # Load fixtures
        call_command('loaddata', *self.fixtures)
        self.client = Client()

    def test_delete_status_failed(self):
        """
        Testing whether a status with tasks linked
        can be removed
        """
        activate('en')
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        status = self.model.objects.get(pk=1)
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
