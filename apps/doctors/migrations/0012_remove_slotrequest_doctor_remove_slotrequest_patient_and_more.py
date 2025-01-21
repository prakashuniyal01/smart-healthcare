# Generated by Django 5.1.5 on 2025-01-21 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0011_doctorleave_slotrequest_weeklyschedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slotrequest',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='slotrequest',
            name='patient',
        ),
        migrations.AlterUniqueTogether(
            name='weeklyschedule',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='weeklyschedule',
            name='doctor',
        ),
        migrations.DeleteModel(
            name='DoctorLeave',
        ),
        migrations.DeleteModel(
            name='SlotRequest',
        ),
        migrations.DeleteModel(
            name='WeeklySchedule',
        ),
    ]
