from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('accounts/', include('allauth.urls')),
    path('registration/', views.registration, name='registration'),
    path('registration/staff', views.registrationStaff, name='registration staff'),
    path('registration/student', views.registrationStudent, name='registration student'),
]