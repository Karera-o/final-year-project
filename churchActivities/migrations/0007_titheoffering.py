# Generated by Django 4.2.1 on 2023-08-27 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('churchActivities', '0006_member_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='TitheOffering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offering_type', models.CharField(choices=[('Tithe', 'Tithe'), ('Offerings', 'Offerings'), ('Umusaruro', 'Umusaruro'), ('Inyubako', 'Inyubako'), ('Iteraniro Rikuru', 'Iteraniro Rikuru')], max_length=50)),
                ('sabbath', models.CharField(choices=[('First Sabbath', 'First Sabbath'), ('Second Sabbath', 'Second Sabbath'), ('Third Sabbath', 'Third Sabbath'), ('Forth Sabbath', 'Forth Sabbath'), ('Fifth Sabbath', 'Fifth Sabbath')], max_length=50)),
                ('returned', models.FloatField()),
                ('date', models.DateField(auto_now=True)),
                ('returner', models.IntegerField()),
            ],
        ),
    ]
