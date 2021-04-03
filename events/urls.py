from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('registration/', views.registration, name='registration'),
    path('registration/staff', views.registrationStaff, name='registration staff'),
    path('registration/student', views.registrationStudent, name='registration student'),
    path('manageEvents', views.manageEvents, name='manageEvents'),
    path('manageEvents/council', views.manageEventsCouncil, name='manageEventsCouncil'),
    path('logout', views.logout, name='logout'),
    path('addEvent', views.add_event, name='addEvent'),
    path('eventRegistration', views.event_registration, name='eventRegistration'),
]