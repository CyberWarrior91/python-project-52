from django.urls import reverse_lazy
from .models import Status
from django.views.generic import ListView, CreateView, UpdateView
from .forms import StatusCreateForm
from django.utils.translation import gettext_lazy as _
from task_manager.mixins.object_crud_mixins import (
    ObjectDeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins.mixins import UserLoginMixin
# Create your views here.


class StatusList(UserLoginMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class StatusCreateView(UserLoginMixin, SuccessMessageMixin, CreateView):
    model = Status
    success_url = reverse_lazy('status_index')
    form_class = StatusCreateForm
    template_name = 'statuses/status_create.html'
    success_message = _('The status was created successfully')


class StatusUpdateView(UserLoginMixin, SuccessMessageMixin, UpdateView):
    success_url = reverse_lazy('status_index')
    model = Status
    form_class = StatusCreateForm
    template_name = 'statuses/status_update.html'
    success_message = _('The status has been updated successfully')


class StatusDeleteView(ObjectDeleteView):
    template_name = 'statuses/status_delete.html'
    success_url = '/statuses/'
    model = Status
    error_message = _("Cannot delete the status, because it's being used")
    success_message = _('The status has been deleted successfully')
