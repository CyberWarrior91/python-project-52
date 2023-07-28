from django.test import TestCase
from .models import CustomUser
from django.core.management import call_command
# Create your tests here.

class UserTestCase(TestCase):
    
    fixtures = ['dumpdata.json']

    def setUp(self):
        # Load fixtures
        call_command('loaddata', *self.fixtures)

    def test_change_user(self):
        user = CustomUser.objects.get(username='Billy333')
        user.first_name = 'Bob'
        user.save()
        self.assertEqual(user.first_name, 'Bob')

    def test_delete_user(self):
        user = CustomUser.objects.get(username='Billy333')
        user.delete()
        self.assertRaises(CustomUser.DoesNotExist, CustomUser.objects.get, username='Billy333')
