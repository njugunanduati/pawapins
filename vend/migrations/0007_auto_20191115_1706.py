# Generated by Django 2.1.7 on 2019-11-15 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vend', '0006_remove_token_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reversal',
            name='amount',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='reversal',
            name='code',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='reversal',
            name='meter',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='reversal',
            name='phone_number',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='reversal',
            name='ref',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='sms',
            name='network_code',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='sms',
            name='to',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='smssent',
            name='cost',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='smssent',
            name='message',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='smssent',
            name='message_id',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='smssent',
            name='status',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='address',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='amount',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='amount_paid',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='description',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='meter',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='pin',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='rct_num',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='reference',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='tarrif',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='tax',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='units',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='units_type',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='vend_time',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
