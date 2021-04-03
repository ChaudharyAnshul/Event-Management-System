from django.shortcuts import render

# Create your views here.


def login(request):
    return render(request, 'Login/login.html')

def dashboard(request):
    return render(request, 'Dashboard/dashboard.html')

def profile(request):
    return render(request, 'Dashboard/profile.html')
    