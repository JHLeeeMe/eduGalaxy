from .models import EduGalaxyUser
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import ugettext as _


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
        choices=(('M', '남자'), ('F', '여자')),
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

# # 회원가입 폼
# class EduGalaxySignupForm(forms.Form):
#
#     User_Email1 = forms.CharField(widget=forms.TextInput, max_length=30, label='이메일')
#     User_Email2 = forms.CharField(widget=forms.TextInput(
#         attrs={'id': 'user_email',
#                'disabled': 'disabled'}
#         ),
#         max_length=30)
#
#     # 이메일 선택 리스트 선택시 Change_Email() 함수 호출
#     Select_Email = forms.CharField(widget=forms.Select(
#         choices=EMAIL_LIST,
#         attrs={
#             'id': 'select',
#             'onchange': 'Change_Email();'}
#         )
#     )
#
#     password1 = forms.CharField(label="비밀번호", widget=forms.PasswordInput)
#     password2 = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput)
#     nickname = forms.CharField(label="닉네임", widget=forms.TextInput)
#
#     # 나이 select 위젯 선언
#     age_list = range(0, 101)
#     AGE_CONTROL = []
#     for age in age_list:
#         if age == 0:
#             AGE_CONTROL.append([age, " "])
#         else:
#             AGE_CONTROL.append([age, str(age)])
#
#     age_choice = forms.CharField(widget=forms.Select(
#         choices=tuple(AGE_CONTROL),
#         attrs={'name': 'age'},
#         ),
#         label='나이'
#     )
#
#     job = forms.CharField(widget=forms.Select(
#         choices=JOB_LIST,
#         attrs={'id': 'job'}
#         ),
#         label="직업"
#     )
#     # 주소는 일단 보류
#
#     # province = AddressSelect.objects.filter().order_by('province').values_list('province', flat=True).distinct()
#     # province_list = [
#     #     ["default", "시/도"]
#     # ]
#     # for provinces in province:
#     #     province_list.append([provinces, provinces])
#     #
#     # province_select = forms.CharField(widget=forms.Select(
#     #     choices=tuple(province_list),
#     #     attrs={'id': 'province'},
#     #     ),
#     #     label='주소'
#     # )
#     #
#     # city_select = forms.CharField(widget=forms.Select(
#     #     choices=[("default", "시/군/구")],
#     #     attrs={'id': 'city'},
#     #     )
#     # )
#     #
#     # dong_select = forms.CharField(widget=forms.Select(
#     #     choices=[("default", "동/면/구")],
#     #     attrs={'id': 'dong'},
#     #     )
#     # )
#
#     # 비밀번호 백엔드 인증
#     def clean_password2(self):
#         password1 = self.cleaned_data['password1']
#         password2 = self.cleaned_data['password2']
#
#         if password1:
#             raise forms.ValidationError('비밀번호를 입력하세요')
#         if password2:
#             raise forms.ValidationError('비밀번호 확인란에 비밀번호를 입력하세요')
#         if password1 != password2:
#             raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
#