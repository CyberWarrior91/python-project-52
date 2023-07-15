from django.urls import path
from task_manager.users.views import UserList, CreateUserView, UserCreateView

urlpatterns = [
    path('', UserList.as_view(), name='index'),
    path('create/', UserCreateView.as_view(), name='users_create'),
]
