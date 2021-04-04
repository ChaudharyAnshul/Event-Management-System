from django.db import models
from django.contrib.auth.models import User as authUser

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

def student_photo_upload(instance, filename):
    return "Photos/Students/{}".format(filename)

class Student(models.Model):
    user = models.ForeignKey(authUser, on_delete= models.CASCADE)
    iid = models.IntegerField()
    dept = models.ForeignKey(Department, on_delete= models.CASCADE)
    division = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    mobile_no = models.IntegerField()
    is_gs = models.BooleanField(default=False) 
    photo = models.FileField(upload_to=student_photo_upload)

    def __str__(self):
        return str(self.user)

def staff_photo_upload(instance, filename):
    return "Photos/Staff/{}".format(filename)

class Staff(models.Model):
    user = models.ForeignKey(authUser, on_delete= models.CASCADE)
    eid = models.IntegerField()
    dept = models.ForeignKey(Department, on_delete= models.CASCADE)
    gender = models.CharField(max_length=10)
    mobile_no = models.IntegerField() 
    designation = models.CharField(max_length=100)
    is_principal = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    photo = models.FileField(upload_to=staff_photo_upload)

    def __str__(self):
        return str(self.user)

class StaffIdMap(models.Model):
    email = models.CharField(max_length=100)
    eid = models.IntegerField()

class StudentIdMap(models.Model):
    email = models.CharField(max_length=100)
    iid = models.IntegerField()

class Council(models.Model):
    name = models.CharField(max_length=100)
    dept = models.ForeignKey(Department, default=None, null=True, on_delete=models.CASCADE)
    is_institute = models.BooleanField(default=False)
    is_department = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    # faculty and student head table 

class FacultyHead(models.Model):
    council = models.ForeignKey(Council, on_delete= models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete= models.CASCADE)

class StudentHead(models.Model):
    council = models.ForeignKey(Council, on_delete= models.CASCADE)
    student = models.ForeignKey(Student, on_delete= models.CASCADE)

class CouncilMember(models.Model):
    council = models.ForeignKey(Council, on_delete= models.CASCADE)
    student = models.ForeignKey(Student, on_delete= models.CASCADE)
    can_edit = models.BooleanField(default=False)

    def __str__(self):
        return str(self.student)

def poster_upload(instance, filename):
    return "Events/Posters/{}".format(filename)

class Event(models.Model):
    name = models.CharField(max_length=100)
    council = models.ForeignKey(Council, on_delete= models.CASCADE)
    is_approved = models.BooleanField(default=False)
    staff_approved =  models.ForeignKey(Staff, on_delete= models.CASCADE, default= None, null= True)
    date = models.DateTimeField()
    description = models.CharField(max_length=2000)
    poster = models.FileField(upload_to=poster_upload)
    registration_fee = models.IntegerField(default=0)
    payment_no = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete= models.CASCADE)
    student = models.ForeignKey(Student, on_delete= models.CASCADE)

class EventWinner(models.Model):
    event = models.ForeignKey(Event, on_delete= models.CASCADE)
    student = models.ForeignKey(Student, on_delete= models.CASCADE)
    place = models.IntegerField()

class UserRoles(models.Model):
    role = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    accept_requests = models.BooleanField(default=False)

    def __str__(self):
        return self.role

class RoleRequests(models.Model):
    user = models.ForeignKey(authUser, on_delete= models.CASCADE)
    role = models.ForeignKey(UserRoles, on_delete= models.CASCADE)
    belongsTo = models.ForeignKey(Council, on_delete= models.CASCADE, default=None, null=True)
    request_time = models.DateTimeField(auto_now_add=True)
    approve_time = models.DateTimeField(null= True, default=None)
    is_approved = models.BooleanField(default=None, null=True)