from django import forms
from django.utils.translation import ugettext as _

from .models import EduGalaxyUser


EMAIL_LIST = (
    ("select", "선택하세요"),
    ("naver.com", "naver.com"),
    ("gmail.com", "gmail.com"),
    ("hanmail.net", "hanmail.net"),
    ("nate.com", "nate.com"),
    ("daum.net", "daum.net"),
    ("hotmail.com", "hotmail.com"),
    ("direct", "직접 입력")
)

JOB_LIST = (
    ("select", "선택하세요"),
    ("초등학생", "초등학생"),
    ("중학생", "중학생"),
    ("고등학생", "고등학생"),
    ("대학생", "대학생"),
    ("대학원생", "대학원생"),
    ("학부모", "학부모"),
    ("학교 관계자", "학교 관게자"),
    ("기타", "기타")
)


class EduGalaxyUserCreationForm(forms.Form):
    user_email1 = forms.CharField(widget=forms.TextInput(
            attrs={
                'autofocus': 'autofocus',
                'required': 'required'}
        ),
        label='이메일'
    )

    user_email2 = forms.CharField(widget=forms.TextInput(
            attrs={
                'id': 'user_email2',
                'disabled': 'disabled'}
        )
    )

    # 이메일 선택 리스트 선택시 Change_Email() 함수 호출
    select_email = forms.CharField(widget=forms.Select(
        choices=EMAIL_LIST,
        attrs={
                'id': 'select',
                'onchange': 'Change_Email();'}
        )
    )

    password1 = forms.CharField(
        label=_("비밀번호"),
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("비밀번호 확인"),
        strip=False,
        widget=forms.PasswordInput,
    )

    user_nickname = forms.CharField(label='닉네임', widget=forms.TextInput)

    # 나이 select 위젯 선언
    age_list = range(0, 101)
    AGE_CONTROL = []
    for age in age_list:
        if age == 0:
            AGE_CONTROL.append([age, " "])
        else:
            AGE_CONTROL.append([age, str(age)])

    user_age = forms.CharField(widget=forms.Select(
            choices=tuple(AGE_CONTROL),
            attrs={'name': 'age'},
        ),
        label='나이'
    )

    user_job = forms.CharField(widget=forms.Select(
            choices=JOB_LIST,
            attrs={'id': 'job'}
        ),
        label="직업"
    )

    user_phone = forms.CharField(label='핸드폰 번호',)
    # checkbox 구현 필요
    user_receive_email = forms.BooleanField(
        label='이메일 수신 동의',
        required=False,
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2


    def save(self, commit=True):

        email1 = self.cleaned_data.get("user_email1")
        email2 = self.cleaned_data.get("user_email2")

        password = self.cleaned_data.get("password1")
        nickname = self.cleaned_data.get("user_nickname")

        str_age = self.cleaned_data.get("user_age")
        job = self.cleaned_data.get("user_job")
        phone = self.cleaned_data.get("user_phone")
        receive_email = self.cleaned_data.get("user_receive_email")

        email = email1 + "@" + email2
        age = int(str_age)

        user = EduGalaxyUser(
            user_email=email,
            password=password,
            user_nickname=nickname,
            user_age=age,
            user_job=job,
            user_phone=phone,
            user_receive_email=receive_email)

        if commit:
            user.save()

        return user

