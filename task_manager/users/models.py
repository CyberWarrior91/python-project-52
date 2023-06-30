from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
class TimestampedModel(models.Model):
    """An abstract model with a pair of timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class User(TimestampedModel):
    username = models.CharField(verbose_name=_('Username'), max_length=200)
    first_name = models.CharField(verbose_name=_('Name'), max_length=200)
    last_name = models.CharField(verbose_name=_('Surname'), max_length=200)
    password = models.CharField(verbose_name=_('Password'), max_length=200)

    def __str__(self):
        return self.nickname
