from django.contrib import admin
from .models import Fcuser, Physician

# Register your models here.
class FcuserAdmin(admin.ModelAdmin):
    list_display = ('email',)

class PhysicianAdmin(admin.ModelAdmin):
    list_diaplay = ('dr_name')

admin.site.register(Fcuser, FcuserAdmin)
admin.site.register(Physician)