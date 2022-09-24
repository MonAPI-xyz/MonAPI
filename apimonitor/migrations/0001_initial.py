# Generated by Django 4.1.1 on 2022-09-20 08:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='APIMonitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('method', models.CharField(choices=[('GET', 'GET'), ('POST', 'POST'), ('PATCH', 'PATCH'), ('PUT', 'PUST'), ('DELETE', 'DELETE')], max_length=16)),
                ('url', models.CharField(max_length=512)),
                ('schedule', models.CharField(choices=[('1MIN', '1 Minute'), ('2MIN', '2 Minute'), ('3MIN', '3 Minute'), ('5MIN', '5 Minute'), ('10MIN', '10 Minute'), ('15MIN', '15 Minute'), ('30MIN', '30 Minute'), ('60MIN', '60 Minute')], max_length=64)),
                ('body_type', models.CharField(choices=[('EMPTY', 'EMPTY'), ('FORM', 'FORM'), ('RAW', 'RAW')], max_length=16)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='APIMonitorResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('execution_time', models.DateTimeField()),
                ('date', models.DateField()),
                ('hour', models.IntegerField()),
                ('minute', models.IntegerField()),
                ('response_time', models.IntegerField()),
                ('success', models.BooleanField()),
                ('log_response', models.TextField()),
                ('monitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='apimonitor.apimonitor')),
            ],
        ),
        migrations.CreateModel(
            name='APIMonitorRawBody',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('monitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raw_body', to='apimonitor.apimonitor')),
            ],
        ),
        migrations.CreateModel(
            name='APIMonitorQueryParam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=64)),
                ('value', models.CharField(max_length=1024)),
                ('monitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='query_params', to='apimonitor.apimonitor')),
            ],
        ),
        migrations.CreateModel(
            name='APIMonitorHeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=64)),
                ('value', models.CharField(max_length=1024)),
                ('monitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='headers', to='apimonitor.apimonitor')),
            ],
        ),
        migrations.CreateModel(
            name='APIMonitorBodyForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=64)),
                ('value', models.CharField(max_length=1024)),
                ('monitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='body_form', to='apimonitor.apimonitor')),
            ],
        ),
    ]
