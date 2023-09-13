from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.models import User
from .forms import NewUserForm, UserUpdateForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from task_manager.mixins.object_crud_mixins import ObjectDeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from task_manager.tasks.models import Task
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


class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    success_url = '/users/'
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_message = _('The user has been updated successfully')

    def get(self, request, *args, **kwargs):
        user_id = request.user.pk
        page_id = kwargs.get('pk')
        if user_id == page_id:
            user = get_object_or_404(self.model, pk=user_id)
            form = self.form_class(instance=user)
            return render(request, self.template_name, context={
                'form': form, 'object_id': user_id, })
        else:
            messages.error(
                request,
                _('You have no rights to modify another user.'), extra_tags='danger'
            )
            return redirect(self.success_url)


class UserDeleteView(ObjectDeleteView):
    template_name = 'users/user_delete.html'
    model = User
    success_url = '/users/'
    success_message = _('The user has been deleted successfully')

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
            messages.error(
                request,
                _('You have no rights to modify another user.'), extra_tags='danger'
            )
            return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        user_id = request.user.pk
        form = self.get_form()
        self.object = get_object_or_404(self.model, pk=user_id)
        user_tasks = Task.objects.filter(Q(creator=self.object) | Q(executor=self.object))
        if user_tasks:
            messages.error(
                request,
                _("Unable to delete the user, because it's being used"),
                extra_tags='danger'
            )
            return redirect(self.success_url)
        else:
            return self.form_valid(form)
