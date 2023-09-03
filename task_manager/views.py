# *task_manager/views.py*
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView
import logging
from django.utils.translation import gettext as _
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import View


logger = logging.getLogger(__name__)

file_handler = logging.FileHandler('errors.log')
file_handler.setLevel(logging.ERROR)

logger.addHandler(file_handler)


class HomePageView(TemplateView):

    template_name = 'index.html'

    def index(self, request):
        logger.error('This is an error message')
        return render(request, HomePageView.template_name)


class UserLoginView(LoginView):
    template_name = 'login.html'
    success_url = '/main/'

    def form_valid(self, form):
        response = super().form_valid(form)
        if not messages.get_messages(self.request):
            messages.success(self.request, _('You have been logged in'))
        return response

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        # Call the parent dispatch method
        response = super().dispatch(request, *args, **kwargs)
        messages.info(request, _('You have been logged out'))
        return response


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


class ObjectCreateView(View):
    success_url = None
    form = None
    create_url = None
    success_message = None

    def get(self, request, *args, **kwargs):
        form = self.form
        return render(request, self.create_url, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return redirect(self.success_url)
        else:
            return render(request, self.create_url, {'form': form})


class ObjectUpdateView(UserLoginMixin, View):
    success_url = None
    model = None
    form = None
    update_url = None
    success_message = None

    def get(self, request, *args, **kwargs):
        object_id = kwargs.get('pk')
        model_object = get_object_or_404(self.model, pk=object_id)
        form = self.form(instance=model_object)
        return render(request, self.update_url, context={
            'form': form, 'object_id': object_id})

    def post(self, request, *args, **kwargs):
        object_id = kwargs.get('pk')
        model_object = get_object_or_404(self.model, pk=object_id)
        form = self.form(request.POST, instance=model_object)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return redirect(self.success_url)
        else:
            return render(
                request,
                self.update_url,
                {'form': form, 'object_id': object_id}
            )


class ObjectDeleteView(UserLoginMixin, DeleteView):
    template_name = None
    success_url = None
    model = None
    error_message = None
    success_message = None

    def post(self, request, *args, **kwargs):
        object_id = kwargs.get('pk')
        self.object = get_object_or_404(self.model, pk=object_id)
        object_tasks = self.object.task_set.all()
        if object_tasks:
            messages.error(self.request, self.error_message, extra_tags='danger')
            return redirect(self.success_url)
        else:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)

    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)
