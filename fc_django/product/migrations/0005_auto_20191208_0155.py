# Generated by Django 2.2.3 on 2019-12-07 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient_info',
            name='unitnumb',
            field=models.CharField(max_length=12, unique=True, verbose_name='등록번호'),
        ),
    ]
