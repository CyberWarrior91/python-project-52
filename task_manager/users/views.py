from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from .models import User
from .forms import NewUserForm, UserUpdateForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from task_manager.tasks.models import Task
from task_manager.mixins.mixins import UserLoginMixin, NoPermission, ObjectIsUsed
# Create your views here.


class UserList(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    success_url = reverse_lazy('login')
    form_class = NewUserForm
    template_name = 'users/user_create.html'
    success_message = _('The user registered successfully')


class UserUpdateView(UserLoginMixin, NoPermission, SuccessMessageMixin, UpdateView):
    success_url = reverse_lazy('users_index')
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_message = _('The user has been updated successfully')


class UserDeleteView(UserLoginMixin, NoPermission, ObjectIsUsed,
                     SuccessMessageMixin, DeleteView):
    template_name = 'users/user_delete.html'
    model = User
    success_url = reverse_lazy('users_index')
    failed_to_delete_msg = _("Unable to delete the user, because it's being used")
    success_message = _('The user has been deleted successfully')

    def get(self, request, *args, **kwargs):
        user_id = request.user.pk
        page_id = kwargs.get('pk')
        if user_id == page_id:
            return render(request, self.template_name, {'user': request.user})
        else:
            return self.no_permission()

    def post(self, request, *args, **kwargs):
        user_id = request.user.pk
        self.object = get_object_or_404(self.model, pk=user_id)
        user_tasks = Task.objects.filter(Q(author=self.object) | Q(executor=self.object))
        if user_tasks:
            return self.unable_to_delete()
        else:
            messages.success(request, self.success_message)
            return self.delete(request)
