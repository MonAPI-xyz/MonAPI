# Generated by Django 4.1.2 on 2022-11-15 07:46

from django.db import migrations, models
import login.models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to=login.models.get_file_path),
        ),
    ]
