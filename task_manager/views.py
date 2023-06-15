# *task_manager/views.py*
from django.shortcuts import render
from django.views.generic.base import TemplateView
import logging
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)

file_handler = logging.FileHandler('errors.log')
file_handler.setLevel(logging.ERROR)

logger.addHandler(file_handler)


class HomePageView(TemplateView):

    template_name = 'index.html'
    
    def index(self, request):
        
        logger.error('This is an error message')
        return render(request, HomePageView.template_name)

def users(request):
    output = _('Users')
    return render(request, 'users.html', context={'output': output})

