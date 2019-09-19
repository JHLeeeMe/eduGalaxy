from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.hashers import check_password
from apps.user.models import EdUser, Temp, SchoolAuth, Log, Profile, Student


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
    ("학교 관계자", "학교 관계자")
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

    def clean(self):
        cleaned_data = super().clean()
        password = self.clean_password2()
        nickname = cleaned_data.get()
        email = self.make_email()

        check_email = EdUser.objects.filler(email=email)
        check_nickname = EdUser.objects.filler(nickname=nickname)
        if check_email.exists():
            raise forms.ValidationError("해당 이메일은 이미 가입하셨습니다.")
        if check_nickname.exists():
            raise forms.ValidationError("존재하는 닉네임입니다.")
        return cleaned_data

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호 오류입니다. 다시 입력해주세요")
        return password2

    def save(self, commit=True):
        email = self.make_email()
        password = self.clean_password2()
        nickname = self.cleaned_data.get("nickname")

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
    phone = forms.CharField(label='핸드폰 번호', widget=forms.TextInput, required=False)
    receive_email = forms.BooleanField(
        label='이메일 수신 동의',
        required=False,
    )
    # 본인인증 여부는 추후 구현 예정(핸드폰 인증/이메일 인증)

    def profile_data(self):
        group = self.cleaned_data.get('group')
        phone = self.cleaned_data.get('phone')
        receive_email = self.cleaned_data.get('receive_email')

        if receive_email:
            data = group + "| " + phone + "| " + "True"
        else:
            data = group + "| " + phone + "| " + "False"
        return data


class StudentCreationForm(forms.Form):
    school = forms.CharField(label='다니는 학교', widget=forms.TextInput)

    grade_list = range(0, 7)
    GRADE = []
    for grade in grade_list:
        if grade == 0:
            GRADE.append([grade, " "])
        else:
            GRADE.append([grade, str(grade)])

    grade = forms.CharField(widget=forms.Select(
        choices=tuple(GRADE),
        attrs={'name': 'grade'},
    ),
        label='학년'
    )

    # 나이 select 위젯 선언
    age_list = range(0, 101)
    AGE_CONTROL = []
    for age in age_list:
        if age == 0:
            AGE_CONTROL.append([age, " "])
        else:
            AGE_CONTROL.append([age, str(age)])

    age = forms.CharField(widget=forms.Select(
            choices=tuple(AGE_CONTROL),
            attrs={'name': 'age'},
        ),
        label='나이'
    )
    address1 = forms.CharField(label='주소', widget=forms.TextInput)
    address2 = forms.CharField(label='상세 주소', widget=forms.TextInput)
    
     # 학력 추가 필요
    def student_data(self, profile):
        school = self.cleaned_data.get('school')
        grade = self.cleaned_data.get('grade')
        age = self.cleaned_data.get('age')
        address1 = self.cleaned_data.get('address1')
        address2 = self.cleaned_data.get('address2')

        student = Student(profile=profile,
                          school=school,
                          grade=grade,
                          age=age,
                          address1=address1,
                          address2=address2)
        return student


class SchoolAuthCreationForm(forms.ModelForm):
    class Meta:
        model = SchoolAuth
        fields = ('school', 'auth_doc', 'tel')

    def __init__(self, *args, **kwargs):
        super(SchoolAuthCreationForm, self).__init__(*args, **kwargs)
        self.fields['auth_doc'].required = False
        self.fields['tel'].required = False

    def school_auth_data(self, profile):
        school = self.cleaned_data.get('school')
        tel = self.cleaned_data.get('tel')
        auth_doc = self.cleaned_data.get('auth_doc')

        school_auth = SchoolAuth(profile=profile,
                                 school=school,
                                 tel=tel,
                                 auth_doc=auth_doc)
        return school_auth


class PasswordChangeForm(forms.Form):
    old_pwd = forms.CharField(
        label=_("기존 비밀번호"),
        strip=False,
        widget=forms.PasswordInput,
    )
    new_pwd1 = forms.CharField(
        label=_("새로운 비밀번호"),
        strip=False,
        widget=forms.PasswordInput,
    )
    new_pwd2 = forms.CharField(
        label=_("비밀번호 확인"),
        strip=False,
        widget=forms.PasswordInput,
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("new_pwd1")
        password2 = self.cleaned_data.get("new_pwd2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 서로 다릅니다!")
        return password2

    def compare_password(self, user):
        old_password = self.cleaned_data.get("old_pwd")
        new_password = self.cleaned_data.get("new_pwd2")

        if not check_password(old_password, user.password):
            raise forms.ValidationError("기존 비밀번호가 아닙니다.")
        if new_password == old_password:
            raise forms.ValidationError("기존 비밀번호와 새로운 비밀번호랑 달라야합니다.")
        return True

    def user_update(self, user):
        if self.compare_password(user):
            password = self.clean_password2()
            user.password = password

            user.set_password(password)
            user.save()


class ProfileUpdateForm(forms.ModelForm):
    school = forms.CharField(label='학교', widget=forms.TextInput)

    grade_list = range(0, 7)
    GRADE = []
    for grade in grade_list:
        if grade == 0:
            GRADE.append([grade, " "])
        else:
            GRADE.append([grade, str(grade)])

    grade = forms.CharField(widget=forms.Select(
        choices=tuple(GRADE),
        attrs={'name': 'grade'},
    ),
        label='학년'
    )

    # 나이 select 위젯 선언
    age_list = range(0, 101)
    AGE_CONTROL = []
    for age in age_list:
        if age == 0:
            AGE_CONTROL.append([age, " "])
        else:
            AGE_CONTROL.append([age, str(age)])

    age = forms.CharField(widget=forms.Select(
        choices=tuple(AGE_CONTROL),
        attrs={'name': 'age'},
    ),
        label='나이'
    )
    address1 = forms.CharField(label='주소', widget=forms.TextInput)
    address2 = forms.CharField(label='상세 주소', widget=forms.TextInput)

    auth_doc = forms.FileField(label='인증서류')
    tel = forms.CharField(label='사무실 연락처', max_length=15)

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['auth_doc'].required = False
        self.fields['tel'].required = False
        self.fields['school'].required = False
        self.fields['grade'].required = False
        self.fields['age'].required = False
        self.fields['address1'].required = False
        self.fields['address2'].required = False

    class Meta:
        model = Profile
        fields = ('phone', 'receive_email')

    def student_save(self, student):
        student.school = self.cleaned_data.get('school')
        student.grade = self.cleaned_data.get('grade')
        student.age = self.cleaned_data.get('age')
        student.address1 = self.cleaned_data.get('address1')
        student.address2 = self.cleaned_data.get('address2')

        student.save()

    def schoolauth_save(self, schoolauth):
        schoolauth.school = self.cleaned_data.get('school')
        schoolauth.tel = self.cleaned_data.get('tel')

        return schoolauth


