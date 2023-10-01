from django.shortcuts import redirect
from .models import Label
from django.views.generic import ListView
from .forms import LabelCreateForm
from django.utils.translation import gettext_lazy as _
from task_manager.mixins.object_crud_mixins import (
    ObjectCreateView,
    ObjectUpdateView,
    ObjectDeleteView
)
from django.contrib import messages
from task_manager.mixins.login_mixin import UserLoginMixin
from task_manager.tasks.models import Task
# Create your views here.


class LabelList(UserLoginMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class LabelCreateView(ObjectCreateView):
    success_url = '/labels/'
    form = LabelCreateForm
    template_name = 'labels/label_create.html'
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

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        labeled_tasks = Task.objects.filter(tasklabel__label_id=label_id)
        if labeled_tasks:
            messages.error(self.request, self.error_message, extra_tags='danger')
            return redirect(self.success_url)
        else:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
