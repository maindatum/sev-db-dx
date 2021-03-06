# Generated by Django 2.2.3 on 2020-02-23 08:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fcuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=15, verbose_name='사용자성명')),
                ('email', models.EmailField(max_length=254, verbose_name='이메일')),
                ('password', models.CharField(max_length=120, null=True, verbose_name='비밀번호')),
                ('level', models.CharField(choices=[('admin', 'admin'), ('user', 'user')], max_length=8, verbose_name='등급')),
                ('register_date', models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')),
            ],
            options={
                'verbose_name': '사용자',
                'db_table': 'fascampus_fcuser',
            },
        ),
        migrations.CreateModel(
            name='Physician',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dr_name', models.CharField(max_length=15, verbose_name='주치의성명')),
                ('email', models.EmailField(max_length=254, verbose_name='이메일')),
                ('comment', models.CharField(blank=True, max_length=15, verbose_name='참고사항')),
                ('register_date', models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_birth', models.DateField()),
                ('residencce', models.CharField(max_length=200)),
                ('grade', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('intro', models.TextField()),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fcuser.University')),
            ],
        ),
    ]
