from django.contrib import admin

from .models import *

# Register your models here.
class Department_Admin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('id', 'name',)
    list_filter = ('name',)

admin.site.register(Department, Department_Admin)

class Staff_Admin(admin.ModelAdmin):
    list_display = ('user', 'eid', 'dept', 'gender', 'mobile_no', 'designation', 'is_principal', 'is_hod', 'photo')
    search_fields = ('user',)
    ordering = ('user', 'eid',)
    list_filter = ('user', 'eid')

admin.site.register(Staff, Staff_Admin)

class Student_Admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'iid', 'dept', 'division', 'gender', 'mobile_no', 'is_gs', 'photo')
    search_fields = ('user',)
    ordering = ('user', 'iid',)
    list_filter = ('user', 'iid')

admin.site.register(Student, Student_Admin)

class Council_Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'dept', 'is_institute', 'is_department', 'is_student',)
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('is_institute', 'is_department', 'is_student')

admin.site.register(Council, Council_Admin)

class FacultyHead_Admin(admin.ModelAdmin):
    list_display = ('id', 'council', 'staff',)
    search_fields = ('staff',)
    ordering = ('staff',)
    list_filter = ('council', 'staff')

admin.site.register(FacultyHead, FacultyHead_Admin)

class StudentHead_Admin(admin.ModelAdmin):
    list_display = ('id', 'council', 'student',)
    search_fields = ('student',)
    ordering = ('student',)
    list_filter = ('council', 'student')

admin.site.register(StudentHead, StudentHead_Admin)

class CouncilMember_Admin(admin.ModelAdmin):
    list_display = ('id', 'council', 'student', 'can_edit')
    search_fields = ('student', 'council')
    ordering = ('student',)
    list_filter = ('council', 'student')

admin.site.register(CouncilMember, CouncilMember_Admin)


class StaffIdMap_Admin(admin.ModelAdmin):
    list_display = ('id', 'eid', 'email')
    search_fields = ('email',)
    ordering = ('eid', 'email',)
    list_filter = ('email', )

admin.site.register(StaffIdMap, StaffIdMap_Admin)

class StudentIdMap_Admin(admin.ModelAdmin):
    list_display = ('id', 'iid', 'email')
    search_fields = ('email',)
    ordering = ('iid', 'email',)
    list_filter = ('email', )

admin.site.register(StudentIdMap, StudentIdMap_Admin)
admin.site.register(UserRoles)

admin.site.register(RoleRequests)