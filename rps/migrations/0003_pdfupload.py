# Generated by Django 4.0 on 2021-12-12 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rps', '0002_student_image_teacher_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='pdfupload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(upload_to='media')),
            ],
        ),
    ]
