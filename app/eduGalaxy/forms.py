from django.contrib.auth.models import User
from .models import EduGalaxyUser
from django.contrib.auth.forms import UserCreationForm
from django import forms


# 회원가입 폼
class EduGalaxySignupForm(forms.ModelForm):

    User_Email1 = forms.CharField(max_length=30)
    User_Email2 = forms.CharField(max_length=30)
    Select_Email = forms.CharField(widget=forms.Select())

    age_list = range(0, 101)
    AGE_CONTROL = []
    for age in age_list:
        if age == 0:
            AGE_CONTROL.append([age, " "])
        else:
            AGE_CONTROL.append([age, str(age)])

    age_choice = forms.CharField(widget=forms.Select(
        choices=tuple(AGE_CONTROL),
        attrs={'name': 'age'},
        ),
        label='나이'
    )

