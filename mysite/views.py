from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView


class HomeTemplateView(TemplateView):
    template_name = 'mysite/index.html'
