# Generated by Django 3.1.5 on 2021-01-27 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0007_auto_20210127_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog1',
            name='data',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='data',
            field=models.JSONField(),
        ),
    ]
