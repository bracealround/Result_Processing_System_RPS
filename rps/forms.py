from django import forms
from rps.models import Course, Enrollment, Assignment


class individual_resultForm(forms.Form):

    registration_no = forms.IntegerField()
    course = forms.ModelChoiceField(queryset=None)
    term_test = forms.DecimalField()
    attendance = forms.IntegerField()
    total_classes = forms.IntegerField()
    semester_final = forms.DecimalField()

    def __init__(self, *args, **kwargs):
        self.teacher = kwargs.pop("teacher")
        print("aaaaaa ", self.teacher)
        super(individual_resultForm, self).__init__(*args, **kwargs)
        self.fields["course"].queryset = Assignment.objects.filter(
            teacher=self.teacher
        )  # More filters to be added. Assignments from zillion years ago should not appear.
        # self.fields["course"].widget = forms.TextField(max_length=100)


class upload_csv_form(forms.Form):

    course = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        self.teacher = kwargs.pop("teacher")
        super(upload_csv_form, self).__init__(*args, **kwargs)
        self.fields["course"].queryset = Assignment.objects.filter(teacher=self.teacher)

        # self.fields["course"].queryset = Course.objects.all().filter(
        #     teacher=self.teacher
        # )


class edit_profile(forms.Form):

    first_name = forms.CharField(max_length=50, widget=None)
    last_name = forms.CharField(max_length=50, widget=None)

    def __init__(self, *args, **kwargs):
        self.first_name = kwargs.pop("first_name")
        self.last_name = kwargs.pop("last_name")
        super(edit_profile, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget = forms.TextInput(
            attrs={"class": "col-md-6", "placeholder": self.first_name}
        )
        self.fields["last_name"].widget = forms.TextInput(
            attrs={"class": "col-md-6", "placeholder": self.last_name}
        )
