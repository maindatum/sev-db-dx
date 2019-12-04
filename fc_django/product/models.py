from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=25, verbose_name='상품명')
    price = models.IntegerField(verbose_name='상품가격')
    description = models.TextField(verbose_name='상품설명')
    stock = models.IntegerField(verbose_name='재고')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

    def __str__(self):
        return self.name

    class Meta:
        db_table ='fascampus_product'
        verbose_name = '상품'

class Diagnosis_0(models.Model):
    dxcode_0 = models.CharField(max_length=20, verbose_name='dxcode_0')
    dxname_0 = models.CharField(max_length=64, verbose_name='dxname_0')

    def __str__(self):
        return self.dxname_0

    class Meta:
        db_table = 'dx_0'
        verbose_name ='진단세부0'

class Diagnosis_1(models.Model):
    dxcode_0 = models.ForeignKey('Diagnosis_0', on_delete=models.CASCADE)
    dxcode_1 = models.CharField(max_length=20, verbose_name='dxcode_1')
    dxname_1 = models.CharField(max_length=64, verbose_name='dxname_1')

    def __str__(self):
        return self.dxname_1

    class Meta:
        db_table = 'dx_1'
        verbose_name ='진단세부1'

class Diagnosis_2(models.Model):
    dxcode_1 = models.ForeignKey('Diagnosis_1', on_delete=models.CASCADE)
    dxcode_2 = models.CharField(max_length=20, verbose_name='dxcode_2')
    dxname_2 = models.CharField(max_length=64, verbose_name='dxname_2')

    def __str__(self):
        return self.dxname_2

    class Meta:
        db_table = 'dx_2'
        verbose_name ='진단세부2'

class Diagnosis_3(models.Model):
    dxcode_2 = models.ForeignKey('Diagnosis_2', on_delete=models.CASCADE)
    dxcode_3 = models.CharField(max_length=20, verbose_name='dxcode_3')
    dxname_3 = models.CharField(max_length=64, verbose_name='dxname_3')

    def __str__(self):
        return self.dxname_3

    class Meta:
        db_table = 'dx_3'
        verbose_name ='진단세부3'

class Patient_info(models.Model):
    unitnumb = models.CharField(max_length=12, verbose_name='등록번호')
    ptname = models.CharField(max_length=48, verbose_name='환자성명')
    birthdate = models.DateField(verbose_name='생년월일')

    def __str__(self):
        return self.ptname

    class Meta:
        db_table = 'pt_info'
        verbose_name ='환자기본정보'

class Pt_diagnosis(models.Model):
    unitnumb = models.ForeignKey('Patient_info', on_delete=models.CASCADE, verbose_name='환자등록번호')
    dx_date = models.DateField(verbose_name='진단일')
    dx_age = models.FloatField(verbose_name='연령')
    dxcode_0 = models.ForeignKey('Diagnosis_0', on_delete=models.CASCADE, verbose_name='진단대분류')
    dxcode_1 = models.ForeignKey('Diagnosis_1', on_delete=models.CASCADE, verbose_name='진단중분류')
    dxcode_2 = models.ForeignKey('Diagnosis_2', on_delete=models.CASCADE, verbose_name='진단소분류')
    dxcode_3 = models.CharField(max_length=40, blank=True, verbose_name='Comment')
    need_confirm = models.BooleanField(verbose_name='컨펌필요여부', default=False)
    compl_confirm = models.BooleanField(verbose_name='컨펌완료여부', default=False)
    dr_name = models.CharField(max_length=40, blank=True, verbose_name='주치의')
    regist_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    regist_user = models.ForeignKey('fcuser.Fcuser', on_delete=models.CASCADE, verbose_name='작성자')

    def __str__(self):
        return str(self.unitnumb_id)

    class Meta:
        db_table = 'pt_diagnosis'
        verbose_name ='환자진단기록'
