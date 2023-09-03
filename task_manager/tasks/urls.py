from django.urls import path
from .views import (
    TaskList,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    SingleTaskView,
)

urlpatterns = [
    path('', TaskList.as_view(), name='task_index'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/', SingleTaskView.as_view(), name='task_single'),
]
