from mysite.models import Task
from members.models import ReminderNotification
from mysite.forms import TaskCreationForm, TaskUpdateForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from datetime import datetime


class HomeTemplateView(TemplateView):
    """
    just a template view for the home page
    """
    template_name = 'mysite/index.html'


@method_decorator(login_required, name='dispatch')
class TaskCreateView(CreateView):
    """
    A create view for the creating a task
    """
    model = Task
    form_class = TaskCreationForm
    template_name = 'mysite/add_task.html'
    success_url = reverse_lazy('mysite:home')

    def post(self, request, *args, **kwargs):
        task_form = TaskCreationForm(request.POST)
        if task_form.is_valid():
            cd = task_form.cleaned_data
            current_user = request.user
            task = Task(title=cd['title'], description=cd['description'],
                        user=current_user, deadline_date=cd['deadline_date'],
                        reminder=cd['reminder']
                        )
            if cd['reminder']:
                if cd['reminder'] > cd['deadline_date']:
                    messages.error(request, "Reminder date can't be after deadline! ")
                    return HttpResponseRedirect(reverse('mysite:add-task', args=(kwargs['slug'], (kwargs['pk']))))
            else:
                messages.error(request, "You have to specify a deadline for your task")
                return HttpResponseRedirect(reverse('mysite:add-task', args=(kwargs['slug'], (kwargs['pk']))))
            task.save()
        return redirect('mysite:home')


@method_decorator(login_required, name='dispatch')
class TaskUpdateView(UpdateView):
    """
    An update view for updating a task
    """
    model = Task
    form_class = TaskUpdateForm
    template_name = 'mysite/edit_task.html'
    success_url = reverse_lazy('mysite:show-all-tasks')

    def post(self, request, *args, **kwargs):
        task_update_form = TaskUpdateForm(request.POST)
        super(TaskUpdateView, self).post(request)  # because I'm using a custom update form super() should be invoked

        if task_update_form.is_valid():
            current_user = request.user
            cd = task_update_form.cleaned_data

            print('deadline:', cd['deadline_date'], 'type:', type(cd['deadline_date']))
            if cd['reminder']:
                if cd['reminder'] > cd['deadline_date']:
                    messages.error(request, "Reminder date can't be after deadline! ")
                    return HttpResponseRedirect(reverse('mysite:edit-task', args=(kwargs['slug'], (kwargs['pk']))))

            updated_task = Task.objects.get(id=kwargs['pk'])
            updated_task.save()
            related_notification = updated_task.task_reminder_notifications.get()
            related_notification.delete()  # because we have to delete the notification related to the unedited task
            # O.W: ReminderNotification.objects.filter(task=task).count() < 1 will be
            # ture and new notification wont be created
            self.object.refresh_from_db()

            return redirect('mysite:show-all-tasks')
        else:
            messages.error(request, "You have to specify a deadline for your task")
            return HttpResponseRedirect(reverse('mysite:edit-task', args=(kwargs['slug'], (kwargs['pk']))))


def mark_as_completed(request, slug, pk):
    """
    When called, the task will be considered as a completed task
    """
    task = Task.objects.get(id=pk, slug=slug)
    task.status = True
    task.save()
    return redirect("mysite:show-all-tasks")


@method_decorator(login_required, name='dispatch')
class TaskListView(ListView):
    """
    Only shows Undone tasks
    """
    model = Task
    template_name = 'mysite/show_tasks.html'

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data()
        undone_tasks = Task.objects.filter(status=False)

        for task in undone_tasks:
            if task.reminder <= datetime.now() < task.deadline_date:  # Checking if datetime.now has passed the
                # task's reminder date or not. If task.reminder <= datetime.now() < task.deadline_date, it means that
                # a notification should be created to reminder the user
                if ReminderNotification.objects.filter(task=task).count() < 1:  # checking whether if there is
                    # already a notification for the task. If there is, no new notification should be created. O.W:
                    # new notification must be created
                    ReminderNotification.objects.create(
                        owner=task.user,
                        message=f'Reminding "{task.title}" deadline:{task.deadline_date}',
                        task=task
                    )

        return context


@method_decorator(login_required, name='dispatch')
class TaskArchiveListView(ListView):
    """
    Shows tasks that are completed
    """
    model = Task
    template_name = 'mysite/show_archive.html'


class NotificationListView(ListView):
    """
    Shows notifications for reminders
    """
    model = ReminderNotification
    template_name = 'mysite/show_notification.html'

    def get_context_data(self, **kwargs):
        context = super(NotificationListView, self).get_context_data()
        not_viewed_notifications = ReminderNotification.objects.filter(owner=self.request.user, views=0)
        context['not_viewed'] = not_viewed_notifications
        context['object_list'] = context['object_list'][::-1]  # to show new notifications first

        for notification in not_viewed_notifications:
            if notification.views < 2:  # checking whether the user has seen the notification or not. Because we
                # don't want multiple notifications for a specific undone task
                notification.views += 1
                notification.save()

        return context
