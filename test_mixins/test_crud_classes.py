from django.urls import reverse_lazy
from task_manager.users.models import User


class ObjectCRUDCase():
    model = None
    pk = None
    index_page = None
    objects_plural = None
    template_name = None

    def test_create_object(self):
        object = self.model.objects.create(name='test name')
        object.save()
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

    def test_objects_list(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        url = reverse_lazy(self.index_page)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        objects = response.context[self.objects_plural]
        for object in objects:
            self.assertIsInstance(object, self.model)
