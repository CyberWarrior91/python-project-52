from .models import Status
from django.views.generic import ListView
from .forms import StatusCreateForm
from django.utils.translation import gettext_lazy as _
from task_manager.mixins.object_crud_mixins import (
    ObjectCreateView,
    ObjectUpdateView,
    ObjectDeleteView
)
from task_manager.mixins.login_mixin import UserLoginMixin
# Create your views here.


class StatusList(UserLoginMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class StatusCreateView(ObjectCreateView):
    success_url = '/statuses/'
    form = StatusCreateForm
    template_name = 'statuses/status_create.html'
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
