from django.urls import path
from mysite import views

app_name = 'mysite'

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('add-task/', views.TaskCreateView.as_view(), name='add-task'),
    path('showing-all-tasks/', views.TaskListView.as_view(), name='show-all-tasks'),
]
