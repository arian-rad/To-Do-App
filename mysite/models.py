from django.db import models
from django.template.defaultfilters import slugify


class Task(models.Model):
    TASK_STATUS = (
        ('done', 'Done'),
        ('undone', 'UnDone'),
    )

    REMINDER_DAYS = (
        (1, 'one day earlier'),
        (2, 'two days earlier'),
        (3, 'three days earlier'),
        (7, 'a weak earlier'),
        (30, 'a month earlier'),
    )

    title = models.CharField(max_length=120, verbose_name='Task Title')
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name='Slug')
    description = models.TextField(max_length=200, verbose_name='Task description')
    deadline_date = models.DateTimeField(verbose_name='Deadline')
    date_edited = models.DateTimeField(auto_now=True, verbose_name='Update Date')
    status = models.CharField(max_length=10, verbose_name='Task Status', choices=TASK_STATUS, default='undone')
    reminder = models.SmallIntegerField(choices=REMINDER_DAYS)

    class Meta:
        verbose_name_plural = 'Tasks'
        ordering = ('-deadline_date',)
        db_table = 'task'

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Task, self).save(**kwargs)
