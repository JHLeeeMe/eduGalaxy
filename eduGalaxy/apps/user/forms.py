from django import forms
from django.utils.translation import ugettext as _

from apps.user.models import Temp


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

GROUP_LIST = (
    ("select", "선택하세요"),
    ("학생", "학생"),
    ("학부모", "학부모"),
    ("학교 관계자", "학교 관게자")
)


class EdUserCreationForm(forms.Form):
    email1 = forms.CharField(widget=forms.TextInput(
            attrs={
                'autofocus': 'autofocus',
                'required': 'required'}
        ),
        label='이메일'
    )

    email2 = forms.CharField(widget=forms.TextInput(
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

    nickname = forms.CharField(label='닉네임', widget=forms.TextInput)

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
        password = self.cleaned_data.get("password1")
        nickname = self.cleaned_data.get("nickname")

        email = self.make_email()

        eduser = email + "| " + password + "| " + nickname
        temp = Temp(eduser=eduser)

        if commit:
            temp.save()

        return temp

    def make_email(self):
        email1 = self.cleaned_data.get("email1")
        email2 = self.cleaned_data.get("email2")
        email = email1 + "@" + email2

        return email


class ProfileCreationForm(forms.Form):
    group = forms.CharField(widget=forms.Select(
            choices=GROUP_LIST,
            attrs={'id': 'group'}
        ),
        label="직업"
    )
    phone = forms.CharField(label='핸드폰 번호', widget=forms.TextInput)
    receive_email = forms.BooleanField(
        label='이메일 수신 동의',
        required=False,
    )
    # 본인인증 여부는 추후 구현 예정(핸드폰 인증/이메일 인증)

    def save(self, commit=True):
        group = self.cleaned_data.get("group")
        phone = self.cleaned_data.get("phone")
        receive_email = self.cleaned_data.get("receive_email")
        pk = self.cleaned_data.get("pk")
        print(type(pk))
        pk = int(pk)

        if receive_email:
            profile = group + "| " + phone + "| " + "True"
        else:
            profile = group + "| " + phone + "| " + "False"

        temp = Temp.objects.get(id=pk)
        temp.profile = profile

        if commit:
            temp.save()

        return temp


    # # 나이 select 위젯 선언
    # age_list = range(0, 101)
    # AGE_CONTROL = []
    # for age in age_list:
    #     if age == 0:
    #         AGE_CONTROL.append([age, " "])
    #     else:
    #         AGE_CONTROL.append([age, str(age)])
    #
    # user_age = forms.CharField(widget=forms.Select(
    #         choices=tuple(AGE_CONTROL),
    #         attrs={'name': 'age'},
    #     ),
    #     label='나이'
    # )
    #
    # user_job = forms.CharField(widget=forms.Select(
    #         choices=JOB_LIST,
    #         attrs={'id': 'job'}
    #     ),
    #     label="직업"
    # )
    #
    # user_phone = forms.CharField(label='핸드폰 번호',)
    # # checkbox 구현 필요
    # user_receive_email = forms.BooleanField(
    #     label='이메일 수신 동의',
    #     required=False,
    # )
    # def save(self, commit=True):
    #
    #     email1 = self.cleaned_data.get("user_email1")
    #     email2 = self.cleaned_data.get("user_email2")
    #
    #     password = self.cleaned_data.get("password1")
    #     nickname = self.cleaned_data.get("user_nickname")
    #
    #     str_age = self.cleaned_data.get("user_age")
    #     job = self.cleaned_data.get("user_job")
    #     phone = self.cleaned_data.get("user_phone")
    #     receive_email = self.cleaned_data.get("user_receive_email")
    #
    #     email = email1 + "@" + email2
    #     age = int(str_age)
    #
    #     user = EduUser(
    #         user_email=email,
    #         password=password,
    #         user_nickname=nickname,
    #         user_age=age,
    #         user_job=job,
    #         user_phone=phone,
    #         user_receive_email=receive_email)
    #
    #     if commit:
    #         user.save()
    #
    #     return user
    #