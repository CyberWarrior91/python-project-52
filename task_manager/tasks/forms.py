from django.forms import ModelForm
from .models import Task
from task_manager.form_class import apply_placeholders
from django.utils.translation import gettext_lazy as _
from django import forms


class TaskCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'name': _('Name'),
            'description': _('Description'),
        }
        apply_placeholders(self, placeholders)

    class Meta:
        model = Task
        fields = ("name", "description", "status",
                  "executor", "labels", 'creator')
        widgets = {'creator': forms.HiddenInput()}
        required = {'description': False, 'executor': False, 'label': False}
