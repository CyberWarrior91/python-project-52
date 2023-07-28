from typing import Any
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import NewUserForm, UserUpdateForm
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest, HttpResponse


# Create your views here.
class UserLoginMixin(LoginRequiredMixin):
    permission_denied_message = _('You are not authorized! Please login to the system.')
    permission_denied_url = reverse_lazy('login')

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message(), extra_tags='danger')
        return redirect(self.permission_denied_url)


class UserList(ListView):
    model = CustomUser
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
            user = CustomUser.objects.get(pk=user_id)
            form = UserUpdateForm(instance=user)
            return render(request, 'users/user_update.html', context={
                'form': form, 'user_id':user_id, })
        else:
            messages.error(request, _('You have no rights to modify another user.'), extra_tags='danger')
            return redirect(self.success_url)
    

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = CustomUser.objects.get(pk=user_id)
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _('The user has been updated successfully'))
            return redirect(self.success_url)
        else:
            return render(request, 'users/user_update.html', {'form': form, 'user_id':user_id,})


class UserDeleteView(UserLoginMixin, DeleteView):
    template_name = 'users/user_delete.html'
    model = CustomUser
    success_url = '/users/'

    def get(self, request, *args, **kwargs):
        user_id = request.user.pk
        page_id = kwargs.get('pk')
        if user_id == page_id:
            self.object = self.model.objects.get(pk=user_id)
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            messages.error(request, _('You have no rights to modify another user.'), extra_tags='danger')
            return redirect(self.success_url)
    
    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, _('The user has been deleted successfully'))
        return redirect(self.success_url)
        