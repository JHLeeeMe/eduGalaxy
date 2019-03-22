from .models import EduGalaxyUser
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import ugettext as _
# from .validators import RegisteredEmailValidator


class EduGalaxyUserCreationForm(UserCreationForm):
    user_email = forms.EmailField(
        label='이메일',
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
    )
    user_nickname = forms.CharField(label='닉네임',)
    user_age = forms.IntegerField(label='나이',)
    user_job = forms.CharField(label='직업',)
    user_sex = forms.ChoiceField(
        choices=((0, '남자'), (1, '여자')),
        label='성별',
    )
    user_address1 = forms.CharField(label='주소1',)
    user_address2 = forms.CharField(label='주소2',)
    user_phone = forms.CharField(label='핸드폰 번호',)
    user_receive_email = forms.BooleanField(
        label='이메일 수신 동의',
    )

    class Meta:
        model = EduGalaxyUser
        fields = ['user_email',
                  'password1',
                  'password2',
                  'user_nickname',
                  'user_age',
                  'user_job',
                  'user_sex',
                  'user_address1',
                  'user_address2',
                  'user_phone',
                  'user_receive_email']


# class VerificationEmailForm(forms.Form):
#     user_email = forms.EmailField(
#         validators=forms.EmailField.default_validators + [RegisteredEmailValidator()],
#         widget=forms.EmailInput(attrs={'autofocus': True})
#     )
