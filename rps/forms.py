from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelect
from rps.models import Course, Enrollment, Assignment, Teacher


class FakeRelation:
    def __init__(self, model):
        self.model = model


class CustomAutocompleteSelect(AutocompleteSelect):
    def __init__(self, model, admin_site, attrs=None, choices=(), using=None):
        rel = FakeRelation(model)
        super().__init__(rel, admin_site, attrs=attrs, choices=choices, using=using)


class MyForm(forms.Form):
    DateFrom = forms.DateField(label="From")
    DateTo = forms.DateField(label="To")
    PE1_Name = forms.ModelChoiceField(
        queryset=Enrollment.objects.all(),
        widget=CustomAutocompleteSelect(Enrollment, admin.AdminSite),
    )


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


class select_semester(forms.Form):

    SEMESTER_CHOICES = (
        (0, "All"),
        (1, "1st year 1st semester"),
        (2, "1st year 2nd semester"),
        (3, "2nd year 1st semester"),
        (4, "2nd year 2nd semester"),
        (5, "3rd year 1st semester"),
        (6, "3rd year 2nd semester"),
        (7, "4th year 1st semester"),
        (8, "4th year 2nd semester"),
    )

    semester = forms.ChoiceField(
        choices=SEMESTER_CHOICES,
        label="",
        initial="All",
        widget=forms.Select(),
        required=False,
    )
