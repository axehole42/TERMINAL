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
from django.contrib import admin
from django.urls import path
from dashboard import views #"this is our app"
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render

def custom_logout(request):
    logout(request)
    return render(request, 'dashboard/logout_success.html')
    #return redirect('home')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), #this is the route to the homepage'
    path('about/', views.about_page, name='about'), #this is the route to the about page'
    path('register/', views.register, name='register'), #this is the route to the register page'
    path('profile/', views.profile, name='profile'), #this is the route to the
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html', next_page='/'), name='login'), #login view from django
    path('logout/', custom_logout, name='logout'),  # Custom logout
]



