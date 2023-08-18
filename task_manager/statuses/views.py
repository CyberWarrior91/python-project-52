from django.shortcuts import render, redirect, get_object_or_404
from .models import Status
from django.views.generic import ListView, DeleteView
from django.views import View
from .forms import StatusCreateForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from task_manager.views import UserLoginMixin

# Create your views here.
class StatusList(UserLoginMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'


class StatusCreateView(UserLoginMixin, View):
    success_url = '/statuses/'
    
    def get(self, request, *args, **kwargs):
        form = StatusCreateForm
        return render(request, 'statuses/status_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = StatusCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('The status was created successfully'))
            return redirect(self.success_url)
        else:
            return render(request, 'statuses/status_create.html', {'form': form})

class StatusUpdateView(UserLoginMixin, View):
    success_url = '/statuses/'
    
    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        status = get_object_or_404(Status, pk=status_id)
        form = StatusCreateForm(instance=status)
        return render(request, 'statuses/status_update.html', context={
                'form': form, 'status_id': status_id })
    

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        status = get_object_or_404(Status, pk=status_id)
        form = StatusCreateForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, _('The status has been updated successfully'))
            return redirect(self.success_url)
        else:
            return render(request, 'statuses/status_update.html', {'form': form, 'status_id': status_id})
        

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
