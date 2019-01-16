# Generated by Django 2.1.5 on 2019-01-12 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attends',
            name='date',
        ),
        migrations.AddField(
            model_name='attends',
            name='std_id',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='attendance.Student'),
            preserve_default=False,
        ),
    ]