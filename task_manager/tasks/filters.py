#listings/filters.py
from django_filters import BooleanFilter, ModelChoiceFilter, FilterSet
from .models import Task
from django import forms
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from task_manager.labels.models import Label

class TaskFilter(FilterSet):
    show_my_tasks = BooleanFilter(
        label=_('Show only my tasks'),
        method='filter_show_my_tasks',
        widget=forms.CheckboxInput,
    )

    status = ModelChoiceFilter(label=_('Status'), queryset=Status.objects.all())
    executor = ModelChoiceFilter(label=_('Executor'), queryset=User.objects.all())
    labels = ModelChoiceFilter(label=_('Labels'), queryset=Label.objects.all())

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
        

    def filter_show_my_tasks(self, queryset, name, value):
        if value:
            user = self.request.user  # assuming you have access to the request object
            return queryset.filter(creator=user)
        return queryset
