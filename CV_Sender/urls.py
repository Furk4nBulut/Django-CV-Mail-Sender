# cv_sender/urls.py

from django.contrib import admin
from django.urls import path
from cv_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.send_cv, name='send_cv'),
    path('email-settings/', views.email_settings, name='email_settings')
]
