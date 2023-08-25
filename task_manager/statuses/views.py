from django.shortcuts import render, redirect, get_object_or_404
from .models import Status
from django.views.generic import ListView, DeleteView
from django.views import View
from .forms import StatusCreateForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from task_manager.views import (
    UserLoginMixin, 
    ObjectCreateView, 
    ObjectUpdateView, 
    ObjectDeleteView
)

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
    

class StatusDeleteView(ObjectDeleteView):
    template_name = 'statuses/status_delete.html'
    success_url = '/statuses/'
    model = Status
    error_message = _("Cannot delete the status, because it's being used")
    success_message = _('The status has been deleted successfully')
