# Generated by Django 4.1.1 on 2022-11-15 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_alter_team_description_alter_team_logo'),
        ('apimonitor', '0014_remove_alertsconfiguration_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertsconfiguration',
            name='team',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='login.team'),
        ),
        migrations.AlterField(
            model_name='apimonitor',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.team'),
        ),
    ]