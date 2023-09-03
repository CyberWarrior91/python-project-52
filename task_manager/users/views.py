from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.models import User
from .forms import NewUserForm, UserUpdateForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from task_manager.views import (
    ObjectCreateView,
    ObjectUpdateView,
    ObjectDeleteView
)
from django.db.models import Q
from task_manager.tasks.models import Task
# Create your views here.


class UserList(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(ObjectCreateView):
    success_url = '/login/'
    form = NewUserForm
    create_url = 'users/user_create.html'
    success_message = _('The user registered successfully')


class UserUpdateView(ObjectUpdateView):
    success_url = '/users/'
    model = User
    form = UserUpdateForm
    update_url = 'users/user_update.html'
    success_message = _('The user has been updated successfully')

    def get(self, request, *args, **kwargs):
        user_id = request.user.pk
        page_id = kwargs.get('pk')
        if user_id == page_id:
            user = get_object_or_404(self.model, pk=user_id)
            form = self.form(instance=user)
            return render(request, self.update_url, context={
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
