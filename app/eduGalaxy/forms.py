from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class CreateUserForm(UserCreationForm):
    user_nickname = forms.CharField(max_length=15)
    user_age = forms.IntegerField()
    user_job = forms.CharField(max_length=30)
    user_sex = forms.BooleanField(required=None)
    user_phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ("username", "user_nickname", "password1", "password2",
                  "user_age", "user_job", "user_sex", "user_phone")

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.user_nickname = self.cleaned_data["user_nickname"]
        user.user_age = self.cleaned_data["user_age"]
        user.user_job = self.cleaned_data["user_job"]
        user.user_sex = self.cleaned_data["user_sex"]
        user.user_phone = self.cleaned_data["user_phone"]

        if commit:
            user.save()
        return user

