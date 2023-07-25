from django.urls import path
from task_manager.users.views import UserList, UserCreateView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('', UserList.as_view(), name='index'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),

]
