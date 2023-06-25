from django.shortcuts import render
from .models import User
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .forms import UserForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

# Create your views here.
class UserList(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class CreateUserView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_create.html'
    success_url = '/login/'

    def form_valid(self, form):
        # Save the new user to the database
        messages.success(self.request, _('The user registered successfully'))
        user = form.save(commit=False)
        user.save()
        return super().form_valid(form)
    
