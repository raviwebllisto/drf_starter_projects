# Generated by Django 2.2.7 on 2019-11-29 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20191128_1040'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_name', models.CharField(max_length=50)),
                ('compny', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=60)),
            ],
        ),
    ]
