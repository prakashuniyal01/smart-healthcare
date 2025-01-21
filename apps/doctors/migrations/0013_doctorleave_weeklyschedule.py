# Generated by Django 5.1.5 on 2025-01-21 13:57

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0012_remove_slotrequest_doctor_remove_slotrequest_patient_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorLeave',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('leave_date', models.DateField(unique=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leaves', to='doctors.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='WeeklySchedule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('day_of_week', models.IntegerField()),
                ('start_time', models.TimeField(default='10:00:00')),
                ('end_time', models.TimeField(default='18:00:00')),
                ('is_active', models.BooleanField(default=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weekly_schedule', to='doctors.doctor')),
            ],
            options={
                'unique_together': {('doctor', 'day_of_week')},
            },
        ),
    ]