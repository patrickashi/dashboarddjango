# Generated by Django 5.0.6 on 2024-06-12 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_student_address_student_email_student_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='address',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
