# Generated by Django 4.2.3 on 2023-08-09 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cognitusApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(max_length=255)),
            ],
        ),
    ]
