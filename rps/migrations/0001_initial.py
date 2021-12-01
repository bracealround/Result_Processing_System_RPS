# Generated by Django 3.2.9 on 2021-12-01 04:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_code', models.CharField(max_length=3, null=True, unique=True)),
                ('dept_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rps.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_no', models.IntegerField(unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('session', models.CharField(max_length=20)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rps.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=50)),
                ('semester', models.IntegerField()),
                ('credit_no', models.DecimalField(decimal_places=2, max_digits=20)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rps.department')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rps.teacher')),
            ],
            options={
                'ordering': ['department', 'semester', 'course_code'],
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term_test', models.DecimalField(decimal_places=2, max_digits=20)),
                ('attendance', models.IntegerField(default=0)),
                ('total_attendence', models.IntegerField(default=0)),
                ('other_assesment', models.DecimalField(decimal_places=2, max_digits=20)),
                ('semester_final', models.DecimalField(decimal_places=2, max_digits=20)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rps.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rps.student')),
            ],
            options={
                'unique_together': {('student', 'course')},
            },
        ),
        migrations.AddConstraint(
            model_name='course',
            constraint=models.UniqueConstraint(fields=('course_code', 'department', 'semester'), name='unique_subject'),
        ),
    ]
