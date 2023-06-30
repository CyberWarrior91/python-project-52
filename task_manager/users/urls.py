from django.urls import path
from task_manager.users.views import UserList, CreateUserView

urlpatterns = [
    path('', UserList.as_view(), name='index'),
    path('create/', CreateUserView.as_view(), name='users_create'),
]
