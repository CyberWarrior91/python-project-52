from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Task
from django.views import View
from django.views.generic import CreateView
from .forms import TaskCreateForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from task_manager.mixins.object_crud_mixins import (
    ObjectUpdateView,
    ObjectDeleteView
)
from task_manager.mixins.login_mixin import UserLoginMixin
from .filters import TaskFilter
from django_filters.views import FilterView

# Create your views here.


class TaskList(UserLoginMixin, FilterView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskCreateView(UserLoginMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'tasks/task_create.html'
    success_message = _('The task was created successfully')

    def form_valid(self, form):
        current_user = self.request.user
        form.instance.author = current_user
        messages.success(request=self.request,
                         message=self.success_message)
        return super(TaskCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task_index')


class TaskUpdateView(ObjectUpdateView):
    success_url = '/tasks/'
    model = Task
    form = TaskCreateForm
    update_url = 'tasks/task_update.html'
    success_message = _('The task has been updated successfully')


class TaskDeleteView(ObjectDeleteView):
    template_name = 'tasks/task_delete.html'
    success_url = '/tasks/'
    model = Task
    success_message = _('The task has been deleted successfully')
    error_message = _("Only the author of the task can delete it")

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        self.object = get_object_or_404(self.model, pk=task_id)
        current_user = request.user
        if current_user != self.object.author:
            messages.error(self.request, self.error_message, extra_tags='danger')
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, context={'object': self.object})

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        form = self.get_form()
        self.object = get_object_or_404(self.model, pk=task_id)
        return self.form_valid(form)


class SingleTaskView(UserLoginMixin, View):
    template_name = 'tasks/task_single.html'
    model = Task

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = self.model.objects.get(pk=task_id)
        labels = task.labels.all()
        return render(
            request,
            self.template_name,
            context={'task': task, 'labels': labels}
        )
