from django.shortcuts import render, redirect, get_object_or_404
from .models import Label
from django.views.generic import ListView, DeleteView
from django.views import View
from .forms import LabelCreateForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from task_manager.views import UserLoginMixin
# Create your views here.

class LabelList(UserLoginMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class LabelCreateView(UserLoginMixin, View):
    success_url = '/labels/'
    
    def get(self, request, *args, **kwargs):
        form = LabelCreateForm
        return render(request, 'labels/label_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LabelCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('The label was created successfully'))
            return redirect(self.success_url)
        else:
            return render(request, 'labels/label_create.html', {'form': form})

class LabelUpdateView(UserLoginMixin, View):
    success_url = '/labels/'
    
    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        label = get_object_or_404(Label, pk=label_id)
        form = LabelCreateForm(instance=label)
        return render(request, 'labels/label_update.html', context={
                'form': form, 'label_id': label_id })
    

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        label = get_object_or_404(Label, pk=label_id)
        form = LabelCreateForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, _('The label has been updated successfully'))
            return redirect(self.success_url)
        else:
            return render(request, 'labels/label_update.html', {'form': form, 'label_id': label_id})
        

class LabelDeleteView(UserLoginMixin, DeleteView):

    template_name = 'labels/label_delete.html'
    success_url = '/labels/'
    model = Label

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        self.object = get_object_or_404(Label, pk=label_id)
        label_tasks = self.object.task_set.all()
        if label_tasks:
            messages.error(self.request, _("Cannot delete the label, because it's being used"), extra_tags='danger')
            return redirect(self.success_url)
        else:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)


    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, _('The label has been deleted successfully'))
        return redirect(self.success_url)
