# Generated by Django 2.1.7 on 2019-11-15 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vend', '0008_auto_20191115_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='units',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
