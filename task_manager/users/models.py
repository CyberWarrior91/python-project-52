from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.


class CustomUser(User):

    def __str__(self):
        return self.username

