# Generated by Django 2.1.7 on 2020-08-05 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vend', '0015_auto_20200724_1010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smssent',
            name='status',
        ),
    ]
