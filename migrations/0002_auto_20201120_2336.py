# Generated by Django 3.1 on 2020-11-20 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='email',
            new_name='name',
        ),
    ]
