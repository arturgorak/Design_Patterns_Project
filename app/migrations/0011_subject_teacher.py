# Generated by Django 4.0 on 2021-12-26 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_delete_singleton'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.teacher'),
        ),
    ]
