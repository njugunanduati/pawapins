# Generated by Django 2.1.7 on 2019-12-09 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vend', '0009_auto_20191115_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='reversal',
            name='seq',
            field=models.CharField(default='00001', max_length=5),
        ),
        migrations.AddField(
            model_name='token',
            name='seq',
            field=models.CharField(default='00001', max_length=5),
        ),
    ]
