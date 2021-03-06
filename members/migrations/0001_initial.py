# Generated by Django 3.1.7 on 2021-04-06 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mysite', '0002_auto_20210317_0149'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReminderNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, default='', max_length=200, null=True, verbose_name='message')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_notifications', to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_reminder_notifications', to='mysite.task', verbose_name='task')),
            ],
        ),
    ]
