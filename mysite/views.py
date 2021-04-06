from mysite.models import Task
from members.models import ReminderNotification
from mysite.forms import TaskCreationForm, TaskUpdateForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from datetime import datetime
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView


class HomeTemplateView(TemplateView):
    """
    just a template view for the home page
    """
    template_name = 'mysite/index.html'


@method_decorator(login_required, name='dispatch')
class TaskCreateView(CreateView):
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
            task.save()
        return redirect('mysite:home')


@method_decorator(login_required, name='dispatch')
class TaskUpdateView(UpdateView):
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
            # updated_task = Task(status=cd['status'], title=cd['title'], description=cd['description'],
            #                     user=current_user, deadline_date=cd['deadline_date'],
            #                     reminder=cd['reminder'])

            print("status is:", 'status' in request.POST)
            print("cd_status:", cd['status'])

            if cd['reminder']:
                if cd['reminder'] > cd['deadline_date']:
                    messages.error(request, "Reminder date can't be after deadline! ")
                    return HttpResponseRedirect(reverse('mysite:edit-task', args=(kwargs['slug'], (kwargs['pk']))))

            updated_task = Task.objects.get(id=kwargs['pk'])
            # if 'status' in request.POST:
            #     cd['status'] = True
            updated_task.status = cd['status']
            print('update status is: ', updated_task.status)

            updated_task.save()
            self.object.refresh_from_db()

            return redirect('mysite:show-all-tasks')
        else:
            messages.error(request, "You have to specify a deadline for your task")
            return HttpResponseRedirect(reverse('mysite:edit-task', args=(kwargs['slug'], (kwargs['pk']))))


def mark_as_completed(request, slug, pk):
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
        print(Task.objects.filter(status=False).query)
        # undone_tasks = Task.objects.filter(status=False)
        # print(undone_tasks)
        # for task in undone_tasks:
        #     # if datetime.now() == task.reminder:
        #     # print(datetime.now())
        #     #     ReminderNotification.objects.create(
        #     #         owner=task.user,
        #     #         message=f'Reminding {task.title} deadline:{task.deadline_date}',
        #     #         task=task
        #     #     )
        #     print(datetime.now())
        # print(Task.objects.filter(status=True).query)
        return context


@method_decorator(login_required, name='dispatch')
class TaskArchiveListView(ListView):
    """
    Shows tasks that are completed
    """
    model = Task
    template_name = 'mysite/show_archive.html'

