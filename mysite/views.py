from django.shortcuts import render
from mysite.models import Task
from mysite.forms import TaskCreationForm, TaskUpdateForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView


class HomeTemplateView(TemplateView):
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


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = 'mysite/edit_task.html'
    success_url = reverse_lazy('mysite:show-all-tasks')

    def post(self, request, *args, **kwargs):
        task_update_form = TaskUpdateForm(request.POST)
        super(TaskUpdateView, self).post(request)
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


class TaskListView(ListView):
    model = Task
    template_name = 'mysite/show_tasks.html'
