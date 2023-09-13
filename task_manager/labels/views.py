from .models import Label
from django.views.generic import ListView
from .forms import LabelCreateForm
from django.utils.translation import gettext_lazy as _
from task_manager.mixins.object_crud_mixins import ObjectDeleteView
from task_manager.mixins.login_mixin import UserLoginMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView
# Create your views here.


class LabelList(UserLoginMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class LabelCreateView(UserLoginMixin, SuccessMessageMixin, CreateView):
    model = Label
    success_url = reverse_lazy('label_index')
    form_class = LabelCreateForm
    template_name = 'labels/label_create.html'
    success_message = _('The label was created successfully')


class LabelUpdateView(UserLoginMixin, SuccessMessageMixin, UpdateView):
    success_url = reverse_lazy('label_index')
    model = Label
    form_class = LabelCreateForm
    template_name = 'labels/label_update.html'
    success_message = _('The label has been updated successfully')


class LabelDeleteView(ObjectDeleteView):
    template_name = 'labels/label_delete.html'
    success_url = '/labels/'
    model = Label
    error_message = _("Cannot delete the label, because it's being used")
    success_message = _('The label has been deleted successfully')
