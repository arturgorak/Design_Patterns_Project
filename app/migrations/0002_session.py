# Generated by Django 4.0 on 2021-12-25 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=200, unique=True)),
                ('is_current_session', models.BooleanField(blank=True, default=False, null=True)),
                ('next_session_begins', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
