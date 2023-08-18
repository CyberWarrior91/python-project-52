from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.views.generic import DeleteView
from django.views import View
from .forms import TaskCreateForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from task_manager.views import UserLoginMixin
from .filters import TaskFilter
from django_filters.views import FilterView

# Create your views here.


class TaskList(UserLoginMixin, FilterView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskCreateView(UserLoginMixin, View):
    success_url = '/tasks/'
    
    def get(self, request, *args, **kwargs):
        form = TaskCreateForm
        return render(request, 'tasks/task_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            messages.success(request, _('The task was created successfully'))
            return redirect(self.success_url)
        else:
            return render(request, 'tasks/task_create.html', {'form': form})

class TaskUpdateView(UserLoginMixin, View):
    success_url = '/tasks/'
    
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_id)
        form = TaskCreateForm(instance=task)
        return render(request, 'tasks/task_update.html', context={
                'form': form, 'task_id': task_id })
    

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_id)
        form = TaskCreateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, _('The task has been updated successfully'))
            return redirect(self.success_url)
        else:
            return render(request, 'tasks/task_update.html', {'form': form, 'task_id': task_id})


class TaskDeleteView(UserLoginMixin, DeleteView):

    template_name = 'tasks/task_delete.html'
    success_url = '/tasks/'
    model = Task
    
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        self.object = get_object_or_404(self.model, pk=task_id)
        current_user = request.user
        if current_user != self.object.creator:
            messages.error(self.request, _("Only the author of the task can delete it"), extra_tags='danger')
            return redirect(self.success_url)
        else:
            return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        current_user = request.user
        task_id = kwargs.get('pk')
        form = self.get_form()
        self.object = get_object_or_404(self.model, pk=task_id)
        if current_user == self.object.creator:
            return self.form_valid(form)
        else:
            messages.error(request, _("Only the author of the task can delete it"), extra_tags='danger')
            return redirect(self.success_url)

    
    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, _('The task has been deleted successfully'))
        return redirect(self.success_url)


class SingleTaskView(UserLoginMixin, View):
    template_name = 'tasks/task_single.html'
    model = Task

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = self.model.objects.get(pk=task_id)
        labels = task.labels.all()
        return render(request, self.template_name, context={'task': task, 'labels': labels})
