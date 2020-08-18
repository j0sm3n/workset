from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('weekly/', views.weekly, name='weekly'),
    path('weekly-agent/', views.weekly_agent, name='weekly_agent'),
    path('new-agent/', views.new_agent, name='new_agent'),
    path('agent/<int:cf>', views.agent, name='agent'),
    path('agents/', views.agents, name='agents'),
    path('upload-doc/', views.upload_doc, name='upload_doc'),
]
