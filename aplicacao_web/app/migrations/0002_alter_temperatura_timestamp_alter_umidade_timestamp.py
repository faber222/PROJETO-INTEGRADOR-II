# Generated by Django 4.2.7 on 2023-12-01 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperatura',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='umidade',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
