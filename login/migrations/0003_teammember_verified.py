# Generated by Django 4.1.2 on 2022-11-18 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_alter_team_description_alter_team_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
