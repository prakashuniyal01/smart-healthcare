# Generated by Django 5.1.5 on 2025-01-21 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0009_alter_specialization_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialization',
            name='description',
            field=models.TextField(),
        ),
    ]