# Generated by Django 4.1.1 on 2022-10-18 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apimonitor', '0005_apimonitor_assertion_value_apimonitor_assetion_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='apimonitor',
            name='is_assert_json_schema_only',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='apimonitor',
            name='previous_step',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='apimonitor.apimonitor'),
        ),
        migrations.CreateModel(
            name='AssertionExcludeKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exclude_key', models.CharField(max_length=1024)),
                ('monitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apimonitor.apimonitor')),
            ],
        ),
    ]