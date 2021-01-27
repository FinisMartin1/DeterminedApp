"""Determined URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

import Determined.views as views

urlpatterns = [
    #Data Pages
    path('dashboard/', views.dashboard),
    path('approve_users/', views.approve_users),
    path('course/', views.course_creation),
    path('students/', views.student_work),
    #Web function pages
    path('logout/', views.user_logout),
    path('register/', views.register),
    path('profile/', views.profile),
    path('admin/', admin.site.urls),
    path('login/', views.home),
    path('', views.home),
    path('forgot-password/', auth_views.PasswordResetView.as_view(template_name="forgot-password.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password-reset-sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password-reset-change.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password-reset-complete.html"), name="password_reset_complete"),
    
]