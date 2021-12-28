from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import *
from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseModelFormSet
from django.forms import modelformset_factory


class TeacherAddForm(UserCreationForm):
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Address",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Mobile No.",
    )

    firstname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Firstname",
    )

    lastname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Lastname",
    )

    email = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Email",
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        user.first_name = self.cleaned_data.get('firstname')
        user.last_name = self.cleaned_data.get('lastname')
        user.phone = self.cleaned_data.get('phone')
        user.address = self.cleaned_data.get('address')
        user.email = self.cleaned_data.get('email')
        user.save()

        teacher = Teacher.objects.create(user=user)
        teacher.save()

        return user


class StudentAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Username",
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Address",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Phone number",
    )

    firstname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Firstname",
    )

    lastname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
            }
        ),
        label="Lastname",
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
            }
        ),
        label="Email Address",
    )

    year = forms.CharField(
        widget=forms.Select(
            choices=YEAR,
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        label="Year",
    )

    branch = forms.CharField(
        widget=forms.Select(
            choices=BRANCH,
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        label="Class",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'address', 'phone', 'firstname', 'lastname', 'email', 'year', 'branch']

    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('firstname')
        user.last_name = self.cleaned_data.get('lastname')
        user.phone = self.cleaned_data.get('phone')
        user.email = self.cleaned_data.get('email')
        user.save()
        student = Student.objects.create(user=user, id_number=user.username, year=self.cleaned_data.get('year'),
                                         students_class=self.cleaned_data.get('branch'))
        student.save()
        return user


class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Old password",
        required=True)

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New password",
        required=True)
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm new password",
        required=True)

    class Meta:
        model = User
        fields = ['id', 'password', 'password1', 'password2']

    def clean(self):
        super(ChangePasswordForm, self).clean()
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        id = self.cleaned_data.get('id')
        user = User.objects.get(pk=id)
        if not user.check_password(password):
            self._errors['password'] = self.error_class([
                'Old password don\'t match'])
        if password1 and password1 != password2:
            self._errors['password1'] = self.error_class([
                'Passwords don\'t match'])
        return self.cleaned_data


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Firstname",
        max_length=30,
        required=False)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Lastname",
        max_length=30,
        required=False)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Email",
        max_length=75,
        required=False)
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Phone Number",
        max_length=16,
        required=False)

    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Home Address",
        max_length=200,
        required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'phone', 'address']


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['session']


class SemesterForm(forms.ModelForm):
    semester = forms.CharField(
        widget=forms.Select(
            choices=SEMESTER,
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        label="semester",
    )
    is_current_semester = forms.CharField(
        widget=forms.Select(
            choices=((True, 'Yes'), (False, 'No')),
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        label="is current semester ?",
    )
    session = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'browser-default custom-select',
            }
        ),
        required=True
    )

    next_semester_begins = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'type': 'date',
            }
        ),
        required=True)

    class Meta:
        model = Semester
        fields = ['semester', 'is_current_semester', 'session', 'next_semester_begins']


# class GradeAddForm(forms.ModelForm):
#     student = forms.ModelMultipleChoiceField(
#         queryset=Student.objects.all().order_by('students_class'),
#         widget=forms.CheckboxSelectMultiple,
#         required=True
#     )
#
#     teacher = forms.ModelMultipleChoiceField(
#         queryset=Teacher.objects.all().order_by('user__last_name'),
#         widget=forms.CheckboxSelectMultiple,
#         required=True
#     )
#
#     subject = forms.ModelMultipleChoiceField(
#         queryset=Subject.objects.all().order_by('subjectName'),
#         widget=forms.CheckboxSelectMultiple,
#         required=True
#     )
#
#     date = forms.DateTimeField(
#         widget=forms.TextInput(
#             attrs={
#                 'type': 'date',
#             }
#         ),
#         required=True)
#
#     grade = forms.CharField(
#         widget=forms.Select(
#             choices=GRADE,
#             attrs={
#                 'class': 'browser-default custom-select',
#             }
#         ),
#         label="Grade",
#     )
#
#     weight = forms.CharField(
#         widget=forms.Select(
#             choices=WEIGHT,
#             attrs={
#                 'class': 'browser-default custom-select',
#             }
#         ),
#         label="Weight",
#     )
#
#     comment = forms.CharField(
#         max_length=30,
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         ),
#         label="Add a little comment",
#         required=False,
#     )
#
#     class Meta:
#         model = Subject
#         fields = ['student', 'teacher', 'subject', 'date', 'grade', 'weight', 'comment']

class GradeAddForm(forms.Form):
    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, user, *args, **kwargs):
        print("konstruktor")
        super(GradeAddForm, self).__init__(*args, **kwargs)
        print("konstruktor2")
        self.fields['subject'].queryset = Subject.objects.filter(teacher=user.teacher)
        print("konstruktor3")





EditGrades = modelformset_factory(
    Grade, fields=("grade", "weight", "date", "comment"), extra=0, can_delete=True
)