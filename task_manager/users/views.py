from typing import Any
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User
from .forms import NewUserForm, UserUpdateForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from task_manager.views import UserLoginMixin
from django.db.models import Q
from task_manager.tasks.models import Task
# Create your views here.

class UserList(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(View):
    success_url = '/login/'
    
    def get(self, request, *args, **kwargs):
        form = NewUserForm
        return render(request, 'users/user_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('The user registered successfully'))
            return redirect(self.success_url)
        else:
            return render(request, 'users/user_create.html', {'form': form})

class UserUpdateView(UserLoginMixin, View):
    success_url = '/users/'
    
    def get(self, request, *args, **kwargs):
        user_id = request.user.pk
        page_id = kwargs.get('pk')
        if user_id == page_id:
            user = get_object_or_404(User, pk=user_id)
            form = UserUpdateForm(instance=user)
            return render(request, 'users/user_update.html', context={
                'form': form, 'user_id':user_id, })
        else:
            messages.error(request, _('You have no rights to modify another user.'), extra_tags='danger')
            return redirect(self.success_url)
    

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(pk=user_id)
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _('The user has been updated successfully'))
            return redirect(self.success_url)
        else:
            return render(request, 'users/user_update.html', {'form': form, 'user_id':user_id,})


class UserDeleteView(UserLoginMixin, DeleteView):
    template_name = 'users/user_delete.html'
    model = User
    success_url = '/users/'

    def get(self, request, *args, **kwargs):
        user_id = request.user.pk
        page_id = kwargs.get('pk')
        if user_id == page_id:
            self.object = get_object_or_404(self.model, pk=user_id)
            form = self.get_form()
            
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            messages.error(request, _('You have no rights to modify another user.'), extra_tags='danger')
            return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        user_id = request.user.pk
        form = self.get_form()
        self.object = get_object_or_404(self.model, pk=user_id)
        user_tasks = Task.objects.filter(Q(creator=self.object) | Q(executor=self.object))
        if user_tasks:
            messages.error(request, _("Unable to delete the user, because it's being used"), extra_tags='danger')
            return redirect(self.success_url)
        else:
            return self.form_valid(form)

    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, _('The user has been deleted successfully'))
        return redirect(self.success_url)
        