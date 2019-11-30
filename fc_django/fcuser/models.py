from django.db import models


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
    dr_name = models.CharField(max_length=15, blank=False, verbose_name='의사성명')
    email = models.EmailField(blank=False, verbose_name='이메일')
    comment = models.CharField(max_length=15)
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')
