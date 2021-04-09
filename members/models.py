from django.db import models
from django.contrib.auth.models import User
from mysite.models import Task


class ReminderNotification(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user', related_name='owner_notifications')
    message = models.TextField(max_length=200, default="", blank=True, null=True, verbose_name='message')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='task',
                             related_name='task_reminder_notifications')
    views = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Notification'

    def __str__(self):
        return self.message
