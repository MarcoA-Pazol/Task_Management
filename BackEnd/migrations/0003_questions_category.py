# Generated by Django 5.0.3 on 2024-04-09 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackEnd', '0002_questions'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='category',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
