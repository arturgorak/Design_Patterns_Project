# Generated by Django 4.0 on 2021-12-28 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_remove_teacher_subject_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.subject'),
        ),
    ]