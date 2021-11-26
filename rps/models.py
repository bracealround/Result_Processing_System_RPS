from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#department table
class department(models.Model):
    dept_no=models.IntegerField(primary_key=True)
    dept_name=models.TextField(max_length=50)

    def __str__(self):
        return str(self.dept_name) +" ( " + str(self.dept_no)+ " )"

#student table
class student(models.Model):
    enroll_no=models.TextField(primary_key=True,max_length=20)
    student_dept_no=models.ForeignKey(department,on_delete=models.CASCADE)
    first_name=models.TextField(max_length=50)
    last_name=models.TextField(max_length=50)
    department=models.TextField(max_length=10,default='No')
    session = models.TextField(max_length=20)



    def __str__(self):
        return str(self.first_name) +" " + str(self.last_name)+ " ( "+str(self.enroll_no)+" )" + str(" ") + str(self.department)




class teacher(models.Model):
    teacher_id=models.TextField(primary_key=True,max_length=20)
    teacher_dept_no=models.ForeignKey(department,on_delete=models.CASCADE)
    first_name=models.TextField(max_length=50)
    last_name=models.TextField(max_length=50)
    title=models.TextField(max_length=50)
    department=models.TextField(max_length=10,default='No')



    def __str__(self):
        return str(self.first_name) +" " + str(self.last_name)+ " ( "+str(self.enroll_no)+" )" + str(" ") + str(self.department)

#courses table
class courses(models.Model):
    course_no=models.TextField(primary_key=True,max_length=20)
    course_name=models.TextField(max_length=50,default=models.SET_DEFAULT)
    course_dept_no=models.ForeignKey(department,on_delete=models.CASCADE)
    sem=models.IntegerField()
    credit_no = models.DecimalField(max_digits=20,decimal_places=2)
    teacher=models.ForeignKey(teacher,on_delete=models.PROTECT)
    
    def __str__(self):
        return str(self.course_name) +" ( " + str(self.course_no)+ " )" +str(self.course_dept_no)

    class Meta:
        constraints=[
        models.UniqueConstraint(fields=['course_no','course_dept_no','sem'],name='unique_subject')
        ]
        ordering=['course_dept_no','sem','course_no']
        # unique_together = (('course_no', 'course_dept_no','sem'),)



#marks table
class marks(models.Model):
    marks_enroll_no=models.ForeignKey(student,on_delete=models.CASCADE)
    marks_course_no=models.ForeignKey(courses,on_delete=models.CASCADE)
    term_test=models.DecimalField(max_digits=20,decimal_places=2)
    present_attendence=models.DateTimeField()
    total_attendence=models.DecimalField(max_digits=20,decimal_places=2)
    other_assesment=models.DecimalField(max_digits=20,decimal_places=2)
    semester_final=models.DecimalField(max_digits=20,decimal_places=2) 
    final_result= models.DecimalField(max_digits=20,decimal_places=2)
    #current_cr=models.IntegerField(default=0)
    @property
    def final_result(self):
        final_result = self.term_test + (self.present_attendence/self.total_attendence)*10 + self.other_assesment+(self.semester_final)*0.6
        return sum



    def __str__(self):
        return str(self.marks_enroll_no) +" ( " + str(self.marks_course_no)+ " )"
    class Meta:
        unique_together = (('marks_enroll_no', 'marks_course_no'),)
        
       
class semester(models.Model):
    student = models.ForeignKey(student,on_delete=models.PROTECT)
    marks = models.ForeignKey(marks,on_delete=models.PROTECT)
    


        
#result table
class result(models.Model):
    result_enroll_no=models.ForeignKey(student,on_delete=models.CASCADE)
    sem1=models.FloatField(default=0)
    sem2=models.FloatField(default=0)
    sem3=models.FloatField(default=0)
    sem4=models.FloatField(default=0)
    sem5=models.FloatField(default=0)
    sem6=models.FloatField(default=0)
    sem7=models.FloatField(default=0)
    sem8=models.FloatField(default=0)
    ogpa=models.FloatField(default=0)
    previous_grades=models.FloatField(default=0)
    total_credits=models.IntegerField(default=0)
    result_status=models.TextField(max_length=30,default='None')

    def __str__(self):
        return  str(self.result_enroll_no) + " Sem1 = " + str(self.sem1) + " Sem2 = " + str(self.sem2) + " Sem3 = " + str(self.sem3) + " Sem4 = " + str(self.sem4) + " Sem5 = " + str(self.sem5) + " Sem6 = " + str(self.sem6) + " Sem7 = " + str(self.sem7) + " Sem8 = " + str(self.sem8) + " OGPA = " + str(self.ogpa) +" Result Status = " +str(self.result_status)
 
