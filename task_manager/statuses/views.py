from django.shortcuts import render, redirect, get_object_or_404
from .models import Status
from django.views.generic import ListView, DeleteView
from django.views import View
from .forms import StatusCreateForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from task_manager.views import UserLoginMixin, ObjectCreateView, ObjectUpdateView

# Create your views here.
class StatusList(UserLoginMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class StatusCreateView(ObjectCreateView):
    success_url = '/statuses/'
    form = StatusCreateForm
    create_url = 'statuses/status_create.html'
    success_message = _('The status was created successfully')


class StatusUpdateView(ObjectUpdateView):
    success_url = '/statuses/'
    model = Status
    form = StatusCreateForm
    update_url = 'statuses/status_update.html'
    success_message = _('The status has been updated successfully')


class StatusDeleteView(UserLoginMixin, DeleteView):

    template_name = 'statuses/status_delete.html'
    success_url = '/statuses/'
    model = Status

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        self.object = get_object_or_404(self.model, pk=status_id)
        status_tasks = self.object.task_set.all()
        if status_tasks:
            messages.error(self.request, _("Cannot delete the status, because it's being used"), extra_tags='danger')
            return redirect(self.success_url)
        else:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)

    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, _('The status has been deleted successfully'))
        return redirect(self.success_url)
