# Generated by Django 4.1.2 on 2022-10-19 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apimonitor', '0006_apimonitor_is_assert_json_schema_only_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apimonitor',
            old_name='assetion_type',
            new_name='assertion_type',
        ),
    ]
