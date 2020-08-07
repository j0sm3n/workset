from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('weekly/', views.weekly, name='weekly'),
    path('weekly-agent/', views.weekly_agent, name='weekly_agent')
]
