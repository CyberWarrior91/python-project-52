from django.forms import ModelForm
from .models import Task
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _
from django import forms

class TaskCreateForm(ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'name': _('Name'),
            'description': _('Description'),
        }
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = placeholders.get(field_name, '')

    class Meta:
        model = Task
        fields = ("name", "description", "status",
                  "executor", "labels", 'creator')
        widgets = {'creator': forms.HiddenInput()}
        required = {'description': False, 'executor': False, 'label': False}
