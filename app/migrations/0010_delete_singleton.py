# Generated by Django 4.0 on 2021-12-26 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_director_singleton'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Singleton',
        ),
    ]