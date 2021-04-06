from django.db import models
from django.contrib.auth.models import User
from mysite.models import Task
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class ReminderNotification(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user', related_name='owner_notifications')
    message = models.TextField(max_length=200, default="", blank=True, null=True, verbose_name='message')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='task',
                             related_name='task_reminder_notifications')
