# Generated by Django 4.2.1 on 2023-09-07 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('churchActivities', '0015_budget'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='date_created',
            field=models.DateField(auto_now=True),
        ),
    ]
