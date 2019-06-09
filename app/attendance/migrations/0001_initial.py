# Generated by Django 2.1.5 on 2019-06-06 07:11

import datetime
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Associated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Attends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('time', models.TimeField(default=datetime.time)),
                ('broadcast_attendance', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=30)),
                ('phone_no', phonenumber_field.modelfields.PhoneNumberField(max_length=128, unique=True)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Enroll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendance.Course')),
            ],
        ),
        migrations.CreateModel(
            name='From',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendance.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendance.Course')),
                ('d', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendance.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=30)),
                ('phone_no', phonenumber_field.modelfields.PhoneNumberField(max_length=128, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('pic_location', models.FileField(upload_to='')),
                ('username', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=30)),
                ('phone_no', phonenumber_field.modelfields.PhoneNumberField(max_length=128, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('pic_location', models.FileField(upload_to='')),
                ('username', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Teaches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendance.Course')),
                ('t', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendance.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='worksFor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendance.Department')),
                ('t', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendance.Teacher')),
            ],
        ),
        migrations.AddField(
            model_name='from',
            name='s',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendance.Student', unique=True),
        ),
        migrations.AddField(
            model_name='enroll',
            name='s',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendance.Student'),
        ),
        migrations.AddField(
            model_name='attends',
            name='cl_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.Class'),
        ),
        migrations.AddField(
            model_name='attends',
            name='std_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendance.Student'),
        ),
        migrations.AddField(
            model_name='associated',
            name='clas_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.Class'),
        ),
        migrations.AddField(
            model_name='associated',
            name='course_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendance.Course'),
        ),
        migrations.AddField(
            model_name='associated',
            name='dep_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendance.Department'),
        ),
        migrations.AddField(
            model_name='associated',
            name='t_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendance.Teacher'),
        ),
    ]
