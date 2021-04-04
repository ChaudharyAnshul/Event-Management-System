from django.shortcuts import render, redirect
from django.contrib.auth.models import User as authUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from .models import *
from django.contrib import messages

from datetime import datetime
# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    return render(request, 'Login/login.html')

@login_required(login_url = '/')
def logout(request):
    django_logout(request)
    return redirect('/')

def get_user_data(request):
    user = authUser.objects.get(id = request.user.id)
    can_edit = False
    in_council = False
    councils = None
    if Student.objects.filter(user = user).exists():
        role = Student.objects.get(user = user)
        role_name = 'Student'
        if CouncilMember.objects.filter(student = role).exists():
            in_council = True
            councils = CouncilMember.objects.filter(student = role)
        if CouncilMember.objects.filter(student = role, can_edit=True).exists():
            can_edit = True
    elif Staff.objects.filter(user = user).exists():
        role = Staff.objects.get(user = user)
        role_name = 'Staff'
        if FacultyHead.objects.filter(staff = role).exists():
            in_council = True
            councils = FacultyHead.objects.filter(staff = role)
        if FacultyHead.objects.filter(staff = role).exists():
            can_edit = True

    user_data = {'role':role, 'role_name':role_name, 'can_edit':can_edit, 'councils':councils, 'in_council':in_council}
    
    staff = ''
    is_fac = False
    if Staff.objects.filter(user = request.user.id).exists():
        staff = Staff.objects.get(user = request.user.id)
        if FacultyHead.objects.filter(staff = staff).exists:
            is_fac = True
    user_data.update({'is_fac':is_fac})
    stud = ''
    is_head = False
    if Student.objects.filter(user = request.user.id).exists():
        stud = Student.objects.get(user = request.user.id)
        if StudentHead.objects.filter(student = stud).exists():
            is_head = True
    user_data.update({'is_head':is_head})
    return user_data

@login_required(login_url = '/')
def dashboard(request):
    if request.method == 'GET':
        user_data = get_user_data(request)
        return render(request, 'Dashboard/dashboard.html', user_data)

@login_required(login_url = '/')
def profile(request):
    if request.method == 'GET':
        user_data = get_user_data(request)
        return render(request, 'Dashboard/profile.html', user_data)

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

@login_required(login_url = '/' )   
def manageEvents(request):
    if request.method == 'GET':
        user_data = get_user_data(request)
        return render(request, 'Dashboard/manageEvents.html', user_data)

@login_required(login_url = '/')
def manageEventsCouncil(request, council):
    if request.method == 'GET':
        user_data = get_user_data(request)
        council_obj = Council.objects.get(name = council)
        user_data.update({'sel_council':council})
        events = Event.objects.filter(council = council_obj)
        user_data.update({'events':events})
        return render(request, 'Dashboard/manageEventsCouncil.html', user_data)

@login_required(login_url = '/')
def add_event(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            councli = Council.objects.get(name = request.POST['council'])
            event = Event.objects.create(
                name = request.POST['name'],
                council = councli,
                is_approved = False,
                date = request.POST['date'],
                description = request.POST['description'],
                poster = request.FILES['poster'],
                registration_fee = request.POST['registration_fee'],
                payment_no = request.POST['payment_no'],
                is_active = False
            )
            event.save()
            return redirect('/manageEvents')
        else:
            messages.info(request, 'Wrong Request Method')
    else:
        return redirect('/accounts/google/login')
    
@login_required(login_url = '/')
def event_registration(request, eventId):
    if request.user.is_authenticated:
        if request.method == 'POST':
            event = Event.objects.get(id = eventId)
            student = Student.objects.get(user = request.user.id)
            if EventRegistration.objects.filter(event = event,student = student).exists():
                messages.info(request, 'Already Registered!')
                return redirect('/allEvents')
            else:
                register = EventRegistration.objects.create(
                    event = event,
                    student = student
                )
                register.save()
                return redirect('/dashboard')
        else: 
            messages.info(request, 'Wrong Request Method')
    else:
        return redirect('/accounts/google/login')


@login_required(login_url = '/')
def adminDashboard(request):
    if request.method == 'GET':
        user_data = get_user_data(request)
        return render(request, 'Dashboard/adminDashboard.html',user_data)

@login_required(login_url = '/')
def roleRequest(request):
    if request.method == 'GET':
        user_data = get_user_data(request)
        P_role = UserRoles.objects.get(role='Principal')
        h_role = UserRoles.objects.get(role='HOD')
        f_role = UserRoles.objects.get(role='Faculty Incharge')
        print(P_role)
        user_data.update({'P_role':P_role,'h_role':h_role,'f_role':f_role})
        return render(request, 'Dashboard/roleRequest.html',user_data)

@login_required(login_url = '/')
def approveRequest(request):
    if request.method == 'GET':
        user_data = get_user_data(request)
        requests = RoleRequests.objects.filter(is_approved = None)
        pending_requests = []
        for i in requests:
            if i.user.is_staff == True:
                pending_requests.append(i)
        user_data.update({'pending_requests':pending_requests})
        return render(request, 'Dashboard/approveRequest.html', user_data)

@login_required(login_url = '/')
def allow_requests_staff(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            UserRoles.objects.filter(role=request.POST['principal']).update(accept_requests = request.POST['accept_requests_1'])
            UserRoles.objects.filter(role=request.POST['hod']).update(accept_requests= request.POST['accept_requests_2'])
            UserRoles.objects.filter(role=request.POST['facultyIncharge']).update(accept_requests= request.POST['accept_requests_3'])
            return redirect('/roleRequest')
        else:
            messages.info(request, 'Wrong Request Method')
    else:
        return redirect('/accounts/google/login')

@login_required(login_url = '/')
def allow_requests_gs(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST['gs'] == 'GS':
                UserRoles.objects.filter(role='GS').update(accept_requests= request.POST['accept_requests'])
            return redirect('/studentRoleRequest')
        else:
            messages.info(request, 'Wrong Request Method')
    else:
        return redirect('/accounts/google/login')

@login_required(login_url = '/')
def allow_requests_council_member(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST['council_member'] == 'Council Member':
                UserRoles.objects.filter(role='GS').update(accept_requests= request.POST['accept_requests'])
            return redirect('/studentRoleRequest')
        else:
            messages.info(request, 'Wrong Request Method')
    else:
        return redirect('/accounts/google/login')

@login_required(login_url = '/')
def allow_requests_student_head(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST['student_head'] == 'Student Head':
                UserRoles.objects.filter(role='Student Head').update(accept_requests= request.POST['accept_requests'])
            return redirect('/studentRoleRequest')
        else:
            messages.info(request, 'Wrong Request Method')
    else:
        return redirect('/accounts/google/login')
    
@login_required(login_url = '/')
def approve_requests(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            role = RoleRequests.objects.get(id = request.POST['requestId'])
            RoleRequests.objects.filter(id = request.POST['requestId']).update(is_approved=True)
            # RoleRequests.objects.filter(user= request.user.id).filter(role= role).update(is_approved= request.POST['response'])
            if role.role.role == 'Principal':
                Staff.objects.filter(user= role.user.id).update(is_principal= True)
            elif role.role.role == 'HOD':
                Staff.objects.filter(user= role.user.id).update(is_hod= True)
            elif role.role.role == 'Faculty Incharge':
                faculty = Staff.objects.get(user= role.user.id)
                facultyIncharge = FacultyHead.objects.create(
                    council = role.belongsTo,
                    staff = faculty
                )
                facultyIncharge.save()
        
            return redirect('/approveRequest')
        else:
            messages.info(request, 'Wrong Request Method')
    else:
        return redirect('/accounts/google/login')

def studentApprove_requests(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            role = RoleRequests.objects.get(id = request.POST['requestId'])
            RoleRequests.objects.filter(id = request.POST['requestId']).update(is_approved=True)
            if role.role.role == 'GS':
                Student.objects.filter(user= role.user.id).update(is_gs= True)
            elif role.role.role == 'Council Member':
                student = Student.objects.get(user = role.user.id)
                council_member = CouncilMember.objects.create(
                    council= role.belongsTo,
                    student= student
                )
                council_member.save()
            elif role.role.role == 'Student Head':
                student = Student.objects.get(user = role.user.id)
                student_head = StudentHead.objects.create(
                    council= role.belongsTo,
                    student= student
                )
                student_head.save()
                council_member = CouncilMember.objects.create(
                    council= role.belongsTo,
                    student= student,
                    can_edit= True
                )
                council_member.save()

            return redirect('/studentApproveRequest')
        else:
            messages.info(request, 'Wrong Request Method')
    else:
        return redirect('/accounts/google/login')

@login_required(login_url = '/')
def reject_requests(request):
    if request.method == 'POST':
        role = RoleRequests.objects.get(id = request.POST['requestId'])
        RoleRequests.objects.filter(id = request.POST['requestId']).update(is_approved=False)
    return redirect('/approveRequest')

def studentReject_requests(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            role = RoleRequests.objects.get(id = request.POST['requestId'])
            RoleRequests.objects.filter(id = request.POST['requestId']).update(is_approved=False)
        return redirect('/studentApproveRequest')

@login_required(login_url = '/')
def viewEvents(request, council,eventId):
    if request.method == 'GET':
        user_data = get_user_data(request)
        event = Event.objects.get(id = eventId)
        user_data.update({'event':event})
        return render(request, 'Dashboard/editEvents.html', user_data)
    
@login_required(login_url = '/')
def allEvents(request):
    if request.method == 'GET':
        user_data = get_user_data(request)
        events = Event.objects.filter(is_approved = True, is_active = True)
        user_data.update({'events':events})
        return render(request, 'Dashboard/allEvents.html', user_data)

@login_required(login_url = '/')
def myEvents(request):
    if request.method == 'GET':
        user_data = get_user_data(request)
        student = Student.objects.get(user = request.user.id)
        events = EventRegistration.objects.filter(student = student)
        user_data.update({'events':events}) 
        return render(request, 'Dashboard/myEvents.html', user_data)

@login_required(login_url = '/')
def event(request, eventId):
    if request.method == 'GET':
        user_data = get_user_data(request)
        event = Event.objects.get(id = eventId)
        user_data.update({'event':event})
        user_data.update({'reg':True})
        return render(request, 'Dashboard/event.html',user_data)
    
@login_required(login_url = '/')
def editEvents(request, council, eventId):
    if request.method == 'POST':
        user_data = get_user_data(request)
        coun = Council.objects.get(name = council)
        Event.objects.filter(id = eventId).update(
            name = request.POST['name'],
            council = coun,
            date = request.POST['date'],
            description = request.POST['description'],
            registration_fee = request.POST['registration_fee'],
            payment_no = request.POST['payment_no'],
        )
        return redirect('/manageEvents')

@login_required(login_url = '/') 
def myEventsDetail(request, eventId):
    if request.method == 'GET':
        user_data = get_user_data(request)
        event = Event.objects.get(id = eventId)
        user_data.update({'event':event})
        user_data.update({'reg':False})
        return render(request, 'Dashboard/event.html',user_data)


@login_required(login_url = '/')
def manageRole(request):
    if request.method == 'GET':
        user_data = get_user_data(request)
        return render(request, 'Dashboard/manageRole.html', user_data)

@login_required(login_url = '/') 
def studentRoleRequest(request):
    if request.method == 'GET':
        user_data = get_user_data(request)
        s_role = UserRoles.objects.get(role='Student Head')
        g_role = UserRoles.objects.get(role='GS')
        c_role = UserRoles.objects.get(role='Council Member')
        user_data.update({'s_role':s_role,'g_role':g_role,'c_role':c_role})
        return render(request, 'Dashboard/studentRoleRequest.html', user_data)
    
@login_required(login_url = '/')
def studentApproveRequest(request):
    if request.method == 'GET':
        user_data = get_user_data(request)
        requests = RoleRequests.objects.filter(is_approved = None)
        if Student.objects.filter(user = request.user.id).exists():
            student = Student.objects.get(user = request.user.id)
            council = StudentHead.objects.get(student = student)  
            pending_requests = []
            for i in requests:
                if i.user.is_staff == False and i.role.role == 'Council Member':
                    if i.belongsTo.name == council.council.name:
                        pending_requests.append(i)
            user_data.update({'pending_requests':pending_requests})
            return render(request, 'Dashboard/studentApproveRequest.html', user_data)
        elif Staff.objects.filter(user = request.user.id).exists():
            staff = Staff.objects.get(user = request.user.id)
            council = FacultyHead.objects.get(staff = staff)  
            pending_requests = []
            for i in requests:
                if i.user.is_staff == False and i.role.role == 'Student Head':
                    if i.belongsTo.name == council.council.name:
                        pending_requests.append(i)
            user_data.update({'pending_requests':pending_requests})
            return render(request, 'Dashboard/studentApproveRequest.html', user_data)

@login_required(login_url = '/')
def add_request(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = authUser.objects.get(id= request.user.id)
            role = UserRoles.objects.get(role= request.POST['role'])
            print(request.POST['belongsTo'])
            if request.POST['belongsTo'] != "null":
                council = Council.objects.get(name= request.POST['belongsTo'])
                new_request = RoleRequests.objects.create(
                    user= user,
                    role= role,
                    belongsTo= council,
                )
            else:
                new_request = RoleRequests.objects.create(
                    user= user,
                    role= role,
                )
            new_request.save()
            return redirect('/sendRequest')
        else:
            messages.info(request, 'Wrong Request Method')
    else:
        return redirect('/accounts/google/login')

@login_required(login_url = '/')
def sendRequest(request):
    user_data = get_user_data(request)
    p_status = UserRoles.objects.get(role = 'Principal')
    h_status = UserRoles.objects.get(role = 'HOD') 
    f_status = UserRoles.objects.get(role = 'Faculty Incharge')
    g_status = UserRoles.objects.get(role = 'GS')
    s_status = UserRoles.objects.get(role = 'Student Head')
    c_status = UserRoles.objects.get(role = 'Council Member')
    user_data.update({'p_status': p_status,'h_status': h_status,'f_status': f_status,'g_status': g_status,'s_status': s_status,'c_status': c_status})
    return render(request, 'Dashboard/sendRequest.html', user_data)

@login_required(login_url = '/')
def yourCouncil(request):
    user_data = get_user_data(request)
    return render(request, 'Dashboard/yourCouncil.html', user_data)

@login_required(login_url = '/')
def yourCouncilDetails(request, council):
    user_data = get_user_data(request)
    councilObj = Council.objects.get(name= council)
    events = Event.objects.filter(council= councilObj)
    user_data.update({'events': events})
    council_members = CouncilMember.objects.filter(council=councilObj)
    user_data.update({'councilMembers': council_members})
    return render(request, 'Dashboard/yourCouncilDetails.html', user_data)


@login_required(login_url = '/')
def eventApprove(request):
    user_data = get_user_data(request)
    return render(request, 'Dashboard/eventApprove.html', user_data)

@login_required(login_url = '/')
def councilEventApprove(request, councilId):
    user_data = get_user_data(request)
    events = Event.objects.filter(council = councilId, is_approved = False, is_rejected = False)
    user_data.update({'events': events})
    return render(request, 'Dashboard/councilEventApprove.html', user_data)

@login_required(login_url = '/')
def approve_event(request, councilId):
    if request.method == "POST":
        user = authUser.objects.get(id = request.user.id)
        Event.objects.filter(id = request.POST['eventId']).update(is_approved = True)
        Event.objects.filter(id = request.POST['eventId']).update(is_active = True)
        # Event.objects.filter(id = request.POST['eventId']).update(staff_approved = user)
        return redirect("/councilEventApprove/"+councilId)

@login_required(login_url = '/')
def reject_event(request, councilId):
    if request.method == "POST":
        user = authUser.objects.get(id = request.user.id)
        Event.objects.filter(id = request.POST['eventId']).update(is_rejected = True)
        # Event.objects.filter(id = request.POST['eventId']).update(staff_approved = user)
        return redirect("/councilEventApprove/"+councilId)

@login_required(login_url = '/')
def viewReport(request, councilId, eventId):
    user_data = get_user_data(request)
    event = Event.objects.get(id= eventId)
    if Report.objects.filter(event= eventId).exists():
        report = Report.objects.get(event= eventId)
        user_data.update({'report': report})
        is_report = True
    else:
        is_report = False
    user_data.update({'is_report': is_report})
    user_data.update({'event': event})

    return render(request, 'Dashboard/report.html', user_data)

@login_required(login_url = '/')
def submitReport(request):
    user_data = get_user_data(request)
    event = Event.objects.get(name= request.POST['event'])
    report = Report.objects.create(
        event= event,
        description = request.POST['description']
    )
    report.save()

    return redirect('/manageEvents')
