from django.shortcuts import render, redirect, get_object_or_404
from .models import Label
from django.views.generic import ListView, DeleteView
from django.views import View
from .forms import LabelCreateForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from task_manager.views import UserLoginMixin, ObjectCreateView, ObjectUpdateView
# Create your views here.

class LabelList(UserLoginMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class LabelCreateView(ObjectCreateView):
    success_url = '/labels/'
    form = LabelCreateForm
    create_url = 'labels/label_create.html'
    success_message = _('The label was created successfully')


class LabelUpdateView(ObjectUpdateView):
    success_url = '/labels/'
    model = Label
    form = LabelCreateForm
    update_url = 'labels/label_update.html'
    success_message = _('The label has been updated successfully')
        

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
