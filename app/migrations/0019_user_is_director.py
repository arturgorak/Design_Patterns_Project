# Generated by Django 4.0 on 2021-12-29 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_subject_branch_subject_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_director',
            field=models.BooleanField(default=False),
        ),
    ]