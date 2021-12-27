# Generated by Django 4.0 on 2021-12-26 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_teacher_subject_alter_grade_subject_delete_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='subject',
            field=models.CharField(blank=True, choices=[('biology', 'biology'), ('civics', 'civics'), ('chemistry', 'chemistry'), ('English', 'English'), ('geography', 'geography'), ('German', 'German'), ('mathematics', 'mathematics'), ('physical education', 'physical education'), ('physics', 'physics'), ('Polish', 'Polish'), ('Spanish', 'Spanish')], max_length=30),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='subject',
            field=models.CharField(blank=True, choices=[('biology', 'biology'), ('civics', 'civics'), ('chemistry', 'chemistry'), ('English', 'English'), ('geography', 'geography'), ('German', 'German'), ('mathematics', 'mathematics'), ('physical education', 'physical education'), ('physics', 'physics'), ('Polish', 'Polish'), ('Spanish', 'Spanish')], max_length=30),
        ),
    ]
