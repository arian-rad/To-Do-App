from django.shortcuts import render
from mysite.models import Task
from mysite.forms import TaskCreationForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
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


class TaskListView(ListView):
    model = Task
    template_name = 'mysite/show_tasks.html'