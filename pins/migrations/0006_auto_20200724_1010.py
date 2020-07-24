# Generated by Django 2.1.7 on 2020-07-24 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pins', '0005_auto_20191101_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='cardbatch',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='cardbatch',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='cardpreview',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='cardpreview',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
