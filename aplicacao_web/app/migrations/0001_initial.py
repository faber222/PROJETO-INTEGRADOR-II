# Generated by Django 4.2.7 on 2023-12-01 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Temperatura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperatura', models.DecimalField(decimal_places=2, max_digits=5)),
                ('idEsp', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
            ],
            options={
                'db_table': 'temperatura',
            },
        ),
        migrations.CreateModel(
            name='Umidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('umidade', models.DecimalField(decimal_places=2, max_digits=5)),
                ('idEsp', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
            ],
            options={
                'db_table': 'umidade',
            },
        ),
    ]
