from django.urls import path
from mysite import views

app_name = 'mysite'

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('showing-all-notifications/', views.NotificationListView.as_view(), name='show-notification'),
    path('add-task/', views.TaskCreateView.as_view(), name='add-task'),
    path('showing-all-tasks/', views.TaskListView.as_view(), name='show-all-tasks'),
    path('edit-task/<str:slug>/<int:pk>/', views.TaskUpdateView.as_view(), name='edit-task'),
    path('task-completed/<str:slug>/<int:pk>/', views.mark_as_completed, name='mark-as-completed'),
    path('completed-tasks/', views.TaskArchiveListView.as_view(), name='show-archive'),
]
