# Generated by Django 3.1.7 on 2021-03-16 04:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Task Title')),
                ('slug', models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, max_length=200, null=True, verbose_name='Task description')),
                ('deadline_date', models.DateTimeField(verbose_name='Deadline')),
                ('date_edited', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
                ('status', models.BooleanField(default=False, verbose_name='Task Status')),
                ('reminder', models.DateTimeField(verbose_name='reminder')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tasks', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name_plural': 'Tasks',
                'db_table': 'task',
                'ordering': ('-deadline_date',),
            },
        ),
    ]
