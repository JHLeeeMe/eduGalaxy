from django.forms import ValidationError
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from django.core.mail import send_mail


class EdUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None):

        # 주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성

        try:
            if not email:
                raise ValueError('이메일은 필수 입력 사항입니다.')

            user = self.model(
                email=self.normalize_email(email),
                nickname=nickname,
            )
            user.set_password(password)
            user.save(using=self._db)
            return user
        except:
            raise ValidationError({'적절한 이메일을 입력하세요'})

    def create_superuser(self, email, nickname, password):

        # 주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        # 단, 최상위 사용자이므로 권한을 부여한다.

        try:
            superuser = self.create_user(
                email=email,
                password=password,
                nickname=nickname,
            )
            superuser.is_admin = True
            superuser.save(using=self._db)
            return superuser
        except:
            raise ValidationError({'적절한 이메일을 입력하세요'})


# 필수 입력사항
class EdUser(AbstractBaseUser):

    email = models.EmailField(
        unique=True,
        max_length=50,
        verbose_name='이메일'
    )
    # AbstractBaseUser 를 상속받음으로써 정의해줘야하는 필드
    is_active = models.BooleanField(default=True, verbose_name='활성화 여부')
    is_admin = models.BooleanField(default=False, verbose_name='관리자')

    objects = EdUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    # has_perms, has_module_perms 장고 인증 백엔드에서 사용
    # 사용자 특정 권한 여부
    def has_perm(self, perm, obj=None):
        return True

    # user 가 주어진 앱에 해당 권한이 있는지 확인
    def has_module_perms(self, app_label):
        return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # 관리자 여부
    @property
    def is_staff(self):
        return self.is_admin


# 사용자 프로필 테이블
class Profile(models.Model):
    eduser = models.OneToOneField(EdUser, on_delete=models.CASCADE, primary_key=True)

    group = models.CharField(max_length=30, verbose_name='직업')
    phone = models.CharField(max_length=15, verbose_name='핸드폰 번호')
    receive_email = models.BooleanField(default=False, verbose_name='이메일 수신 여부')
    is_naver = models.BooleanField(default=False, verbose_name='네이버 연동 여부')
    is_google = models.BooleanField(default=False, verbose_name='구글 연동 여부')
    confirm = models.BooleanField(default=False, verbose_name='본인인증 여부')

    class Meta:
        verbose_name = '사용자 프로필'
        verbose_name_plural = '사용자 프로필'

    objects = EdUserManager()


# 학교 관계자 테이블
class SchoolAuth(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)

    school = models.CharField(verbose_name='소속/학교', max_length=20, null=True)
    auth_doc = models.FileField(
        verbose_name='인증 서류',
        upload_to="signup/schoolAuth",
        null=True,
    )
    # form 작업 뒤 null=False, upload 경로 설정 필요
    tel = models.CharField(max_length=15, verbose_name='사무실 연락처', null=True)

    class Meta:
        verbose_name = '학교 관계자'
        verbose_name_plural = '학교 관계자'


# 학생 테이블
class Student(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)

    school = models.CharField(verbose_name='학교', max_length=20, null=False)
    grade = models.IntegerField(default=0, verbose_name='학년', null=True)
    age = models.IntegerField(default=0, verbose_name='나이')
    gender = models.CharField(default='U', max_length=2, verbose_name='성별')
    address1 = models.CharField(max_length=100, verbose_name='주소', null=True)
    address2 = models.CharField(max_length=100, verbose_name='상세주소', null=True)

    class Meta:
        verbose_name = '학생'
        verbose_name_plural = '학생'


# 학부모 테이블
class Parent(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)

    address1 = models.CharField(max_length=100, verbose_name='주소', null=True)
    address2 = models.CharField(max_length=100, verbose_name='상세주소', null=True)

    class Meta:
        verbose_name = '학부모'
        verbose_name_plural = '학부모'


# 자녀 테이블
class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

    school = models.CharField(verbose_name='학교', max_length=20, null=False)
    grade = models.IntegerField(default=0, verbose_name='학년', null=True)
    age = models.IntegerField(default=0, verbose_name='나이')
    gender = models.CharField(default='U', max_length=2, verbose_name='성별')

    class Meta:
        verbose_name = '자녀'
        verbose_name_plural = '자녀'


# 관리자 관리 로그/보안
class Log(models.Model):
    eduser = models.OneToOneField(EdUser, on_delete=models.CASCADE, primary_key=True)

    signup_ip = models.CharField(max_length=20, verbose_name='가입 ip')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='가입날짜')
    login_ip = models.CharField(max_length=20, verbose_name='로그인 ip')
    log_file = models.FileField(verbose_name='로그 파일', null=True)
    # form 작업 뒤 upload 경로 설정 필요

    class Meta:
        verbose_name = 'log'
        verbose_name_plural = 'logs'


class EduLevel(models.Model):
    school = models.CharField(verbose_name='학교', max_length=20, null=False)
    status = models.CharField(verbose_name='상태', max_length=4)

    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE, null=True)

    modified_cnt = models.IntegerField(default=0, verbose_name='수정 횟수')


class Temp(models.Model):
    eduser = models.CharField(verbose_name='기본정보', max_length=100)
    profile = models.CharField(verbose_name='프로필', max_length=100)
    student = models.CharField(verbose_name='학생정보', max_length=250, null=True)
    parent = models.CharField(verbose_name='학부모정보', max_length=200, null=True)
    schoolauth = models.CharField(verbose_name='학교관계자정보', max_length=100, null=True)
    child = models.CharField(verbose_name='자녀정보', max_length=100, null=True)
    create_date = models.DateTimeField(verbose_name='생성날짜', blank=True, null=True)
