from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DeleteView
from django.contrib.messages.views import SuccessMessageMixin


class UserLoginMixin(LoginRequiredMixin):
    permission_denied_message = _('You are not authorized! Please login to the system.')
    permission_denied_url = reverse_lazy('login')

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(
            self.request,
            self.get_permission_denied_message(),
            extra_tags='danger'
        )
        return redirect(self.permission_denied_url)


class NoPermission:
    model = None
    template_name = None
    success_url = None
    form_class = None

    def get(self, request, *args, **kwargs):
        user_id = request.user.pk
        page_id = kwargs.get('pk')
        if user_id == page_id:
            user = get_object_or_404(self.model, pk=user_id)
            form = self.form_class(instance=user)
            return render(request, self.template_name, context={
                'form': form, 'object_id': user_id, })
        else:
            return self.no_permission()

    def no_permission(self):
        messages.error(
            self.request,
            _('You have no rights to modify another user.'),
            extra_tags='danger'
        )
        return redirect(self.success_url)


class ObjectIsUsed:
    failed_to_delete_msg = None
    success_url = None

    def unable_to_delete(self) -> HttpResponseRedirect:
        messages.error(
            self.request,
            self.failed_to_delete_msg,
            extra_tags='danger'
        )
        return redirect(self.success_url)


class DeleteUsedObject(UserLoginMixin, ObjectIsUsed, SuccessMessageMixin, DeleteView):
    template_name = None
    success_url = None
    model = None
    failed_to_delete_msg = None
    success_message = None

    def post(self, request, *args, **kwargs):
        object_id = kwargs.get('pk')
        object = get_object_or_404(self.model, pk=object_id)
        object_tasks = object.task_set.all()
        if object_tasks:
            return self.unable_to_delete()
        else:
            object.delete()
            messages.success(request, self.success_message)
            return redirect(self.success_url)
