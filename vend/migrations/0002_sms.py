# Generated by Django 2.1.7 on 2019-10-29 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateField(auto_now=True)),
                ('date_recieved', models.CharField(max_length=300, null=True)),
                ('msisdn', models.CharField(max_length=20, null=True)),
                ('at_id', models.CharField(max_length=300)),
                ('linkId', models.CharField(max_length=300)),
                ('message', models.CharField(max_length=300)),
                ('to', models.CharField(max_length=300)),
                ('networkCode', models.CharField(max_length=300)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
