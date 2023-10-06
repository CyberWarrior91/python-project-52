from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Label
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import LabelCreateForm
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from task_manager.mixins.mixins import ObjectIsUsed, UserLoginMixin
from task_manager.tasks.models import Task
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


class LabelDeleteView(UserLoginMixin, ObjectIsUsed, SuccessMessageMixin, DeleteView):
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('label_index')
    model = Label
    failed_to_delete_msg = _("Cannot delete the label, because it's being used")
    success_message = _('The label has been deleted successfully')

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        self.object = get_object_or_404(self.model, pk=label_id)
        labeled_tasks = Task.objects.filter(tasklabel__label_id=label_id)
        if labeled_tasks:
            return self.unable_to_delete()
        else:
            self.object.delete()
            messages.success(request, self.success_message)
            return redirect(self.success_url)
