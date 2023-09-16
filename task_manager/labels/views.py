from .models import Label
from django.views.generic import ListView
from .forms import LabelCreateForm
from django.utils.translation import gettext_lazy as _
from task_manager.mixins.object_crud_mixins import (
    ObjectCreateView,
    ObjectUpdateView,
    ObjectDeleteView
)
from task_manager.mixins.login_mixin import UserLoginMixin
# Create your views here.


class LabelList(UserLoginMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class LabelCreateView(ObjectCreateView):
    success_url = '/labels/'
    form = LabelCreateForm
    create_url = 'labels/label_create.html'
    success_message = _('The label was created successfully')


class LabelUpdateView(ObjectUpdateView):
    success_url = '/labels/'
    model = Label
    form = LabelCreateForm
    update_url = 'labels/label_update.html'
    success_message = _('The label has been updated successfully')


class LabelDeleteView(ObjectDeleteView):
    template_name = 'labels/label_delete.html'
    success_url = '/labels/'
    model = Label
    error_message = _("Cannot delete the label, because it's being used")
    success_message = _('The label has been deleted successfully')
