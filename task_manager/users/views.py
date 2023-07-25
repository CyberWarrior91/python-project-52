from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import NewUserForm, UserUpdateForm
from django.contrib import messages
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.
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

class UserUpdateView(PermissionRequiredMixin, View):
    success_url = '/users/'
    permission_required = 'users.change_customuser'

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = CustomUser.objects.get(pk=user_id)
        form = UserUpdateForm(instance=user)
        return render(request, 'users/user_update.html', context={
            'form': form, 'user_id':user_id, })

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


class UserDeleteView(DeleteView):
    template_name = 'users/user_delete.html'
    model = CustomUser
    success_url = '/users/'
    
    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, _('The user has been deleted successfully'))
        return redirect(self.success_url)
        