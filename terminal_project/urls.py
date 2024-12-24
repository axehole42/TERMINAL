"""
URL configuration for terminal_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
"""
URL configuration for terminal_project project.
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from dashboard.views import rss_feed_json, rss_feed

# Import only the functions you actually have in dashboard/views.py
from dashboard.views import (
    home,
    about_page,
    register,
    profile,
    rss_feed,  # <- Make sure to import this, matching your function name in views.py
)

def custom_logout(request):
    logout(request)
    return render(request, 'dashboard/logout_success.html')
    # return redirect('home')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),         # Route for your homepage
    path('about/', about_page, name='about'), 
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(
        template_name='dashboard/login.html', 
        next_page='/'
    ), name='login'),
    path('logout/', custom_logout, name='logout'),  
    path('rss/', rss_feed, name='rss_feed'),  # Using rss_feed from dashboard/views.py
     path("rss/json/", rss_feed_json, name="rss_feed_json"),  # new JSON endpoint
]



