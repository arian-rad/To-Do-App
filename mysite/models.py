from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Task(models.Model):
    TASK_STATUS = (
        ('done', 'Done'),
        ('undone', 'UnDone'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='user_tasks')
    title = models.CharField(max_length=120, verbose_name='Task Title')
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name='Slug')
    description = models.TextField(max_length=200, verbose_name='Task description', blank=True, null=True)
    deadline_date = models.DateTimeField(verbose_name='Deadline')
    date_edited = models.DateTimeField(auto_now=True, verbose_name='Update Date')
    status = models.BooleanField(verbose_name='Task Status', default=False)
    reminder = models.DateTimeField(verbose_name='reminder', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Tasks'
        ordering = ('-deadline_date',)
        db_table = 'task'

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Task, self).save(**kwargs)
