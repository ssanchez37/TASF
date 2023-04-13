from django.urls import path
from . import views

app_name = 'KPI'
urlpatterns = [
    path('', views.simple_upload, name='index'),
]