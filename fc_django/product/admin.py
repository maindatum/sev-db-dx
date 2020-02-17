from django.contrib import admin
from .models import Product, Diagnosis_0, Diagnosis_1, Diagnosis_2, Diagnosis_3, Patient_info, Pt_diagnosis, Book
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price')

admin.site.register(Product, ProductAdmin)

class Diagnosis_0_Admin(admin.ModelAdmin):
    list_display = ('dxcode_0', 'dxname_0')
    pass

admin.site.register(Diagnosis_0, Diagnosis_0_Admin)

class Diagnosis_1_Admin(admin.ModelAdmin):
    list_display = ('dxcode_0','dxcode_1', 'dxname_1')
    pass

admin.site.register(Diagnosis_1, Diagnosis_1_Admin)

class Diagnosis_2_Admin(admin.ModelAdmin):
    list_display = ('dxcode_1','dxcode_2', 'dxname_2')
    pass

admin.site.register(Diagnosis_2, Diagnosis_2_Admin)

class Diagnosis_3_Admin(admin.ModelAdmin):
    list_display = ('dxcode_2','dxcode_3', 'dxname_3')
    pass

admin.site.register(Diagnosis_3, Diagnosis_3_Admin)

class Pt_diagnosis_Admin(admin.ModelAdmin):
    list_display = ('unitnumb', 'dxcode_0','dxcode_1','dxcode_2','dxcode_3','regist_dttm', 'regist_user')
    pass

admin.site.register(Pt_diagnosis, Pt_diagnosis_Admin)


class Patient_info_Admin(admin.ModelAdmin):
    list_display = ('unitnumb', 'ptname','birthdate')
    pass

admin.site.register(Patient_info, Patient_info_Admin)

class Book_Admin(admin.ModelAdmin):
    list_display = ('title', 'publication_date','author')
    pass

admin.site.register(Book, Book_Admin)