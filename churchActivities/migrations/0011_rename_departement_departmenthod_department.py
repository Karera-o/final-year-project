# Generated by Django 4.2.1 on 2023-09-04 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('churchActivities', '0010_remove_department_hod_alter_titheoffering_quarter_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='departmenthod',
            old_name='departement',
            new_name='department',
        ),
    ]
