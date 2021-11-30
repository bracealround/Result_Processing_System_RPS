# Generated by Django 3.2.9 on 2021-11-30 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rps', '0007_alter_course_course_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['department', 'semester', 'course_code']},
        ),
        migrations.RemoveConstraint(
            model_name='course',
            name='unique_subject',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='course_no',
            new_name='course_code',
        ),
        migrations.AddConstraint(
            model_name='course',
            constraint=models.UniqueConstraint(fields=('course_code', 'department', 'semester'), name='unique_subject'),
        ),
    ]