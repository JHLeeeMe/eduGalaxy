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
    user_email1 = forms.CharField(widget=forms.TextInput, label='이메일')
    user_email2 = forms.CharField(widget=forms.TextInput(
            attrs={
                'id': 'user_email',
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

    # 주소, 성별 보류
    # user_gender = forms.ChoiceField(
    #     choices=(('M', '남자'), ('F', '여자')),
    #     label='성별',
    # )

    # province = AddressSelect.objects.filter().order_by('province').values_list('province', flat=True).distinct()
    # province_list = [
        #     ["default", "시/도"]
        # ]
        # for provinces in province:
        #     province_list.append([provinces, provinces])
        #
        # province_select = forms.CharField(widget=forms.Select(
        #     choices=tuple(province_list),
        #     attrs={'id': 'province'},
        #     ),
        #     label='주소'
        # )
        #
        # city_select = forms.CharField(widget=forms.Select(
        #     choices=[("default", "시/군/구")],
        #     attrs={'id': 'city'},
        #     )
        # )
        #
        # dong_select = forms.CharField(widget=forms.Select(
        #     choices=[("default", "동/면/구")],
        #     attrs={'id': 'dong'},
        #     )
        # )

    user_phone = forms.CharField(label='핸드폰 번호',)
    # checkbox 구현 필요
    user_receive_email = forms.BooleanField(
        label='이메일 수신 동의',
    )
