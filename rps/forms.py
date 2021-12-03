from django import forms

class individual_resultForm(forms.Form):
    reg_no = forms.CharField(max_length=100)
    course_code = forms.CharField(max_length=100)
    term_text_marks = forms.IntegerField()
    attendence = forms.IntegerField()
    total_attendence = forms.IntegerField()
    other_assesment = forms.IntegerField()
    final_result = forms.IntegerField()

