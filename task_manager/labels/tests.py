from django.test import TestCase
from .models import Label
from django.core.management import call_command
# Create your tests here.

class UserTestCase(TestCase):
    
    fixtures = ['fixtures/labeldata.json']

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
