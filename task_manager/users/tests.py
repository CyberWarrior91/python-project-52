from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
# Create your tests here.


class UserTestCase(TestCase):

    fixtures = ['fixtures/userdata.json']

    def setUp(self):
        # Load fixtures
        call_command('loaddata', *self.fixtures)

    def test_create_user(self):
        user = User.objects.create(
            first_name='Ben',
            last_name='Green',
            username='Billy333'
        )
        user.save()
        self.assertTrue(User.objects.filter(username='Billy333').exists())

    def test_change_user(self):
        user = User.objects.get(username='Vlad')
        user.first_name = 'Bob'
        user.save()
        self.assertEqual(user.first_name, 'Bob')

    def test_delete_user(self):
        user = User.objects.get(username='Vlad')
        user.delete()
        self.assertRaises(User.DoesNotExist, User.objects.get, username='Vlad')
