from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Fcuser(models.Model):
    username = models.CharField(max_length=15, blank=False, verbose_name='사용자성명')
    email = models.EmailField(blank=False, verbose_name='이메일')
    password = models.CharField(max_length=120, null=True, verbose_name='비밀번호')
    level = models.CharField(max_length=8, verbose_name='등급',
                             choices=(
                                 ('admin', 'admin'),
                                 ('user', 'user')
                             )
                             )
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'fascampus_fcuser'
        verbose_name = '사용자'


class Physician(models.Model):
    dr_name = models.CharField(max_length=15, blank=False, verbose_name='주치의성명')
    email = models.EmailField(blank=False, verbose_name='이메일')
    comment = models.CharField(max_length=15, blank=True, verbose_name='참고사항')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

    def __str__(self):
        return self.dr_name

class University(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    date_birth = models.DateField()
    residencce = models.CharField(max_length=200)
    # photo = models.ImageField(blank=True)
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    intro = models.TextField()