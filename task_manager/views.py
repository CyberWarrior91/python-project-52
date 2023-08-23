# *task_manager/views.py*
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
import logging
from django.utils.translation import gettext as _
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect


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
        messages.error(self.request, self.get_permission_denied_message(), extra_tags='danger')
        return redirect(self.permission_denied_url)