from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
class TimestampedModel(models.Model):
    """An abstract model with a pair of timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)


class User(TimestampedModel):
    nickname = models.CharField(verbose_name=_('Username'), db_column='username', max_length=200) # username of the user
    name = models.CharField(verbose_name=_('Name'), max_length=200)
    surname = models.CharField(verbose_name=_('Surname'), max_length=200) # full name
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.nickname
