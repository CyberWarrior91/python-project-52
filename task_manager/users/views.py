from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .forms import NewUserForm
from django.contrib import messages
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


# Create your views here.
class UserList(ListView):
    model = CustomUser
    template_name = 'users/index.html'
    context_object_name = 'users'


class CreateUserView(CreateView):
    model = CustomUser
    form_class = NewUserForm
    template_name = 'users/user_create.html'
    success_url = '/login/'
    def form_valid(self, form):
        messages.success(self.request, _('The user registered successfully'))
        return super().form_valid(form)


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
