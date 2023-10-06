from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Status
from .forms import StatusCreateForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins.mixins import UserLoginMixin, ObjectIsUsed
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


class StatusDeleteView(UserLoginMixin, ObjectIsUsed, SuccessMessageMixin, DeleteView):
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('status_index')
    model = Status
    failed_to_delete_msg = _("Cannot delete the status, because it's being used")
    success_message = _('The status has been deleted successfully')

    def post(self, request, *args, **kwargs):
        object_id = kwargs.get('pk')
        object = get_object_or_404(self.model, pk=object_id)
        object_tasks = object.task_set.all()
        if object_tasks:
            return self.unable_to_delete()
        else:
            object.delete()
            messages.success(request, self.success_message)
            return redirect(self.success_url)
