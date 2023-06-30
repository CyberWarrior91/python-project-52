# *task_manager/views.py*
from django.shortcuts import render
from django.views.generic.base import TemplateView
import logging
from django.utils.translation import gettext as _
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages


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
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy('main')

    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


def users_create(request):
    return render(request, 'registration.html')


