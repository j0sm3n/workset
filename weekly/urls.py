from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('weekly/', views.weekly, name='weekly'),
    path('weekly-agent/', views.weekly_agent, name='weekly_agent'),
    path('new-agent/', views.new_agent, name='new_agent'),
    path('new-form-agent/', views.new_form_agent, name='new_form_agent'),
    path('save-agent/', views.save_agent, name='save_agent'),
    path('agent/<int:cf>', views.agent, name='agent'),
    path('agents/', views.agents, name='agents'),
    path('upload-doc/', views.upload_doc, name='upload_doc'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
