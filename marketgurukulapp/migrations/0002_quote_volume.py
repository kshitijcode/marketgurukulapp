# Generated by Django 2.2.6 on 2020-05-01 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketgurukulapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='volume',
            field=models.IntegerField(default=0),
        ),
    ]
