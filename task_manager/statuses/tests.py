from django.test import TestCase
from .models import Status
from django.core.management import call_command
# Create your tests here.


class UserTestCase(TestCase):

    fixtures = ['fixtures/statusdata.json']

    def setUp(self):
        # Load fixtures
        call_command('loaddata', *self.fixtures)

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
