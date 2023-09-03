from task_manager.form_class import ObjectCreateForm
from .models import Status
from django.utils.translation import gettext_lazy as _


class StatusCreateForm(ObjectCreateForm):

    class Meta:
        model = Status
        fields = ['name']
        labels = {
            'name': _('Name'),
        }
