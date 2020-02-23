from django.contrib import admin
from .models import Fcuser, Physician, University, Student
from .forms import StudentForm

# Register your models here.
class FcuserAdmin(admin.ModelAdmin):
    list_display = ('email',)

class PhysicianAdmin(admin.ModelAdmin):
    list_diaplay = ('dr_name')
#
# @admin.register(Fcuser)
# class CountryAmin(admin.ModelAdmin):
#     form = UniversityForm

@admin.register(Student)
class StudentAmin(admin.ModelAdmin):
    form = StudentForm

admin.site.register(Fcuser, FcuserAdmin)
admin.site.register(Physician)