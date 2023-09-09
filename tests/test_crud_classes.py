from django.test import TestCase, Client
from django.core.management import call_command


class ObjectCRUDCase():
    model = None
    pk = None

    def test_create_object(self):
        label = self.model.objects.create(name='test name')
        label.save()
        self.assertTrue(self.model.objects.filter(name='test name').exists())

    def test_change_object(self):
        object = self.model.objects.get(pk=self.pk)
        object.name = 'test name'
        object.save()
        self.assertEqual(object.name, 'test name')

    def test_delete_object(self):
        object = self.model.objects.get(pk=self.pk)
        object.delete()
        self.assertRaises(self.model.DoesNotExist, self.model.objects.get, pk=self.pk)
