from django.urls import path
from mysite import views

app_name = 'mysite'

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
]
