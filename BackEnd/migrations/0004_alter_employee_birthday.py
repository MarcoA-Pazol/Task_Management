# Generated by Django 5.0.3 on 2024-05-11 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackEnd', '0003_alter_employee_birthday_alter_employee_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='birthday',
            field=models.DateField(default='2024-01-01'),
        ),
    ]
