# Generated by Django 5.0.3 on 2024-05-10 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackEnd', '0009_employee_occupation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='occupation',
            field=models.CharField(choices=[('Back-End', 'Back-End Developer'), ('Graphic Design', 'Graphic Desinger'), ('User Experience Design', 'UX Designer')], default=None, max_length=50, null=True),
        ),
    ]
