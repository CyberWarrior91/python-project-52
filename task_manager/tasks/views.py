from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.views import View
from .forms import TaskCreateForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from task_manager.views import (
    UserLoginMixin,
    ObjectCreateView,
    ObjectUpdateView,
    ObjectDeleteView
)
from .filters import TaskFilter
from django_filters.views import FilterView

# Create your views here.


class TaskList(UserLoginMixin, FilterView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskCreateView(ObjectCreateView):
    success_url = '/tasks/'
    form = TaskCreateForm
    create_url = 'tasks/task_create.html'
    success_message = _('The task was created successfully')

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            form.save_m2m()
            messages.success(request, self.success_message)
            return redirect(self.success_url)
        else:
            return render(request, self.create_url, {'form': form})


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
        if current_user != self.object.creator:
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
