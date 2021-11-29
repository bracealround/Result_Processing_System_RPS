# Generated by Django 3.2.9 on 2021-11-29 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rps', '0003_auto_20211129_0206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_no', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('course_name', models.CharField(default=django.db.models.deletion.SET_DEFAULT, max_length=50)),
                ('sem', models.IntegerField()),
                ('credit_no', models.DecimalField(decimal_places=2, max_digits=20)),
                ('course_dept_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rps.department')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rps.teacher')),
            ],
            options={
                'ordering': ['course_dept_no', 'sem', 'course_no'],
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term_test', models.DecimalField(decimal_places=2, max_digits=20)),
                ('attendance', models.IntegerField(default=0)),
                ('total_attendence', models.DecimalField(decimal_places=2, max_digits=20)),
                ('other_assesment', models.DecimalField(decimal_places=2, max_digits=20)),
                ('semester_final', models.DecimalField(decimal_places=2, max_digits=20)),
                ('mark_course_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rps.course')),
                ('mark_registration_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rps.student')),
            ],
            options={
                'unique_together': {('mark_registration_no', 'mark_course_no')},
            },
        ),
        migrations.AddConstraint(
            model_name='course',
            constraint=models.UniqueConstraint(fields=('course_no', 'course_dept_no', 'sem'), name='unique_subject'),
        ),
    ]
