from .models import Label
from task_manager.form_class import ObjectCreateForm
from django.utils.translation import gettext_lazy as _


class LabelCreateForm(ObjectCreateForm):

    class Meta:
        model = Label
        fields = ['name']
        labels = {
            'name': _('Name'),
        }
