from django.forms import ModelForm
from .models import Task
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class TaskCreateForm(ModelForm):
       def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.helper = FormHelper()
           self.helper.layout = Layout(
               Field('name', css_class='form-label'),
               Field('description', css_class='form-label'),
               Field('status', css_class='form-label'),
               Field('executor', css_class='form-label'),
               Field('labels', css_class='form-label'),
           )

       class Meta:
           model = Task
           fields = ['name', 'description', 'status', 'executor', 'labels']
