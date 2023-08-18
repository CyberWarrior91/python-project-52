from django.urls import path
from .views import StatusList, StatusCreateView, StatusUpdateView, StatusDeleteView

urlpatterns = [
    path('', StatusList.as_view(), name='status_index'),
    path('create/', StatusCreateView.as_view(), name='status_create'),
    path('<int:pk>/update/', StatusUpdateView.as_view(), name='status_update'),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name='status_delete'),
]
