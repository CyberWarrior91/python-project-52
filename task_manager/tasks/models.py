from django.db import models
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from task_manager.labels.models import Label
from django.utils import timezone
# Create your models here.


class Task(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    creator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='+',
        blank=True
    )
    executor = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    labels = models.ManyToManyField(Label, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
