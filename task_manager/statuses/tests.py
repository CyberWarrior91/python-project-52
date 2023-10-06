from django.test import TestCase, Client
from .models import Status
from task_manager.users.models import User
from task_manager.tasks.models import Task
from django.core.management import call_command
from django.urls import reverse_lazy
from django.contrib.messages import get_messages
from django.utils.translation import activate
from test_mixins.mixin_for_crud_tests import ObjectCRUDCase
from test_mixins.mixin_for_form_test import ObjectFormTest
from .forms import StatusCreateForm
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
        Task.objects.create(name='test', author=user, status=status)
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
            "Невозможно удалить статус, потому что он используется"
        )


class CreateStatusFormCase(TestCase, ObjectFormTest):
    form = StatusCreateForm
    correct_data = {
        'name': 'test status'
    }
