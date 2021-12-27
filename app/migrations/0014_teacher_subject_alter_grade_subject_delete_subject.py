# Generated by Django 4.0 on 2021-12-26 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_student_students_class_alter_student_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='subject',
            field=models.CharField(blank=True, choices=[('mathematics', 'mathematics'), ('Polish', 'Polish'), ('English', 'English'), ('geography', 'geography'), ('biology', 'biology'), ('chemistry', 'chemistry'), ('physics', 'physics'), ('physical education', 'physical education'), ('civics', 'civics'), ('German', 'German'), ('Spanish', 'Spanish')], max_length=30),
        ),
        migrations.AlterField(
            model_name='grade',
            name='subject',
            field=models.CharField(blank=True, choices=[('mathematics', 'mathematics'), ('Polish', 'Polish'), ('English', 'English'), ('geography', 'geography'), ('biology', 'biology'), ('chemistry', 'chemistry'), ('physics', 'physics'), ('physical education', 'physical education'), ('civics', 'civics'), ('German', 'German'), ('Spanish', 'Spanish')], max_length=30),
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
    ]
