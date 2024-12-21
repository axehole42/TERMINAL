from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from django.templatetags.static import static

def home(request):
    if request.user.is_authenticated:
        # Show personalized dashboard for logged-in users
        context = {
            'username': request.user.username,
            'description': 'Welcome to your customizable dashboard!',
            'stream_url': static('dashboard/videos/phoenix-us.m3u8'),  # Replace with your stream URL
        }
        return render(request, 'dashboard/home.html', context)
    else:
        # Show registration form for unauthenticated users
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                login(request, user)  # Automatically log in the user
                return redirect('home')  # Redirect to the dashboard
        else:
            form = RegistrationForm()
        
        # Show a general welcome message and the registration form
        context = {
            'welcome_message': 'Welcome to the Tsonevski Terminal.',
            'info_message': (
                "To access the terminal's advanced features, please "
                "<a href='/login/'>log in</a> or "
                "<a href='/register/'>register</a> for an account."
            ),
            'form': form,
        }
        return render(request, 'dashboard/home.html', context)

# Create your views here.
def about_page(request):
    return render(request, 'dashboard/about.html')

# Our login page function.
def register(request):
    print("Register view called")  # Debug statement
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('home')  # Redirect to the home page
    else:
        form = RegistrationForm()
    return render(request, 'dashboard/register.html', {'form': form, 'content_container': False})

def profile(request):
    return render(request, 'dashboard/profile.html')