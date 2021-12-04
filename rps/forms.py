from django import forms
from rps.models import Course


class individual_resultForm(forms.Form):

    reg_no = forms.CharField(max_length=100)
    course = forms.ModelChoiceField(queryset=None)
    term_text_marks = forms.IntegerField()
    attendence = forms.IntegerField()
    total_attendence = forms.IntegerField()
    other_assesment = forms.IntegerField()
    semester_final = forms.IntegerField()

    def __init__(self, teacher=None, *args, **kwargs):
        super(individual_resultForm, self).__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.all().filter(teacher=teacher)
        # self.fields["course"].widget = forms.TextField(max_length=100)


class upload_csv_form(forms.Form):

    course = forms.ModelChoiceField(queryset=None)

    def __init__(self, teacher=None, *args, **kwargs):
        super(upload_csv_form, self).__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.all().filter(teacher=teacher)
