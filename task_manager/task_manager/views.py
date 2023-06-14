# *task_manager/views.py*
from django.shortcuts import render
from django.views.generic.base import TemplateView

class HomePageView(TemplateView):

    template_name = 'index.html'
    
    def index(self, request):
        return render(request, HomePageView.template_name)
