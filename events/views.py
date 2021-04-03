from django.shortcuts import render, redirect
from django.contrib.auth.models import User as authUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import *
from django.contrib import messages
# Create your views here.


def login(request):
    return render(request, 'Login/login.html')

@login_required(login_url = '/')
def logout(request):
    logout(request)
    return redirect('/')

@login_required(login_url = '/')
def dashboard(request):
    if request.method == 'GET':
        user = authUser.objects.get(id = request.user.id)
        can_edit = False
        in_council = False
        if Student.objects.filter(user = user).exists():
            role = Student.objects.get(user = user)
            role_name = 'Student'
            if CouncilMember.objects.filter(student = role).exists():
                in_council = True
            if CouncilMember.objects.filter(student = role, can_edit=True).exists():
                can_edit = True
        elif Staff.objects.filter(user = user).exists():
            role = Staff.objects.get(user = user)
            role_name = 'Staff'
            if FacultyHead.objects.filter(staff = role).exists():
                can_edit = True
        return render(request, 'Dashboard/dashboard.html', {'role':role, 'role_name':role_name, 'can_edit':can_edit, 'in_council':in_council})

@login_required(login_url = '/')
def profile(request):
    if request.method == 'GET':
        user = authUser.objects.get(id = request.user.id)
        can_edit = False
        in_council = False
        if Student.objects.filter(user = user).exists():
            role = Student.objects.get(user = user)
            role_name = 'Student'
            if CouncilMember.objects.filter(student = role).exists():
                in_council = True
            if CouncilMember.objects.filter(student = role).exists():
                can_edit = True
        elif Staff.objects.filter(user = user).exists():
            role = Staff.objects.get(user = user)
            role_name = 'Staff'
            if FacultyHead.objects.filter(staff = role).exists():
                can_edit = True
        return render(request, 'Dashboard/profile.html', {'role':role, 'role_name':role_name, 'can_edit':can_edit, 'in_council':in_council})

@login_required(login_url = '/')
def registration(request):
    if request.user.is_authenticated:
        if not Student.objects.filter(user = request.user.id).exists() and not Staff.objects.filter(user = request.user.id).exists():
            return render(request, 'Login/register.html')
        else:
            return redirect('/dashboard')
    else:
        return redirect('/')

@login_required(login_url = '/')
def registrationStaff(request):
    if request.method == 'POST':
        dept = Department.objects.get(name = request.POST['department'])
        eid = request.POST['eid']
        if StaffIdMap.objects.filter(eid = eid, email = request.user.email).exists():
            staff = Staff.objects.create(
                user = authUser.objects.get(id = request.user.id),
                eid = eid,
                dept = dept,
                gender = request.POST['gender'],
                mobile_no = request.POST['mobile'],
                designation = request.POST['Designation'],
                photo = request.FILES['photo']  
            )
            staff.save()
            user = authUser.objects.get(id = request.user.id)
            user.is_staff = True
            user.save()
            return redirect('/dashboard')
        else:
            messages.info(request, 'Incorrect Employee ID')
            return redirect('/registration')

@login_required(login_url = '/')
def registrationStudent(request):
    if request.method == 'POST':
        dept = Department.objects.get(name = request.POST['department'])
        iid = request.POST['iid']
        if StudentIdMap.objects.filter(iid = iid, email = request.user.email).exists():
            student = Student.objects.create(
                user = authUser.objects.get(id = request.user.id),
                iid = iid,
                dept = dept,
                division = request.POST['division'],
                gender = request.POST['gender'],
                mobile_no = request.POST['mobile'],
                photo = request.FILES['photo']
            )
            student.save()
            return redirect('/dashboard')
        else:
            messages.info(request, 'Incorrect Institute ID')
            return redirect('/registration')
    
def manageEvents(request):
    return render(request, 'Dashboard/manageEvents.html')

def manageEventsCouncil(request):
    return render(request, 'Dashboard/manageEventsCouncil.html')

def add_event(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            event = Event.objects.create(
                name = request.POST['name'],
                council = request.POST['council'],
                is_approved = False,
                date = request.POST['date'],
                description = request.POST['description'],
                poster = request.FILES['poster'],
                registration_fee = request.POST['registration_fee'],
                payment_no = request.POST['payment_no'],
                is_active = False
            )
            event.save()
            return redirect('/dashboard')
        else:
            messages.info(request, 'Wrong Request Method')
    else:
        return redirect('/accounts/google/login')

def event_registration(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            register = EventRegistration.objects.create(
                event = request.POST['event'],
                student = request.user.id
            )
            register.save()
            return redirect('/dashboard')
        else: 
            messages.info(request, 'Wrong Request Method')
    else:
        return redirect('/accounts/google/login')
