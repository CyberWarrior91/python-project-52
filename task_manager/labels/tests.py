from django.test import TestCase
from .models import Label
from django.core.management import call_command
from task_manager.users.models import User
from django.contrib.messages import get_messages
from django.utils.translation import activate
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.urls import reverse_lazy
from test_mixins.mixin_for_crud_tests import ObjectCRUDCase
from test_mixins.mixin_for_form_test import ObjectFormTest
from .forms import LabelCreateForm
# Create your tests here.


class LabelTestCase(TestCase, ObjectCRUDCase):

    fixtures = [
        'fixtures/labeldata.json',
        'fixtures/userdata.json',
    ]
    pk = 2
    model = Label
    index_page = 'label_index'
    objects_plural = 'labels'
    template_name = 'labels/index.html'

    def setUp(self):
        # Load fixtures
        call_command('loaddata', *self.fixtures)
        activate('en')

    def test_delete_label_failed(self):
        """
        Testing whether a label with tasks linked
        can be removed
        """

        user = User.objects.get(pk=1)
        self.client.force_login(user)
        label = Label.objects.get(pk=2)
        test_task = Task.objects.create(
            name='test',
            author=user,
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
            "Невозможно удалить метку, потому что она используется"
        )


class CreateLabelFormCase(TestCase, ObjectFormTest):
    form = LabelCreateForm
    correct_data = {
        'name': 'test label'
    }
