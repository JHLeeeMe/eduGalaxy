from django.forms import ValidationError
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone


class EduGalaxyUserManager(BaseUserManager):
    def create_user(self, user_email, user_nickname, password=None):

        # 주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성

        try:
            if not user_email:
                raise ValueError('이메일은 필수 입력 사항입니다.')

            user = self.model(
                user_email=self.normalize_email(user_email),
                user_nickname=user_nickname,
            )
            user.set_password(password)
            user.is_active = True
            user.save(using=self._db)
            return user
        except:
            raise ValidationError({'적절한 이메일을 입력하세요'})

    def create_superuser(self, user_email, user_nickname, password):

        # 주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        # 단, 최상위 사용자이므로 권한을 부여한다.

        try:
            superuser = self.create_user(
                user_email=user_email,
                password=password,
                user_nickname=user_nickname,
            )
            superuser.is_admin = True
            superuser.is_active = True
            superuser.save(using=self._db)
            return superuser
        except:
            raise ValidationError({'적절한 이메일을 입력하세요'})


class EduGalaxyUser(AbstractBaseUser):
    # 필수 입력사항
    user_email = models.EmailField(
        unique=True,
        max_length=50,
        verbose_name='이메일'
    )
    user_nickname = models.CharField(
        unique=True,
        max_length=20,
        verbose_name='닉네임',
        null=False
    )

    # 상세 입력 사항
    user_age = models.IntegerField(default=0, verbose_name='나이')
    user_job = models.CharField(max_length=30, verbose_name='직업')
    user_sex = models.BooleanField(default=False, verbose_name='성별')
    user_address1 = models.CharField(max_length=100)
    user_address2 = models.CharField(max_length=100)
    user_phone = models.CharField(max_length=15, verbose_name='핸드폰 번호')
    user_receive_email = models.BooleanField(default=False, verbose_name='알림 동의 여부')

    # 관리자 필요 데이터
    user_confirm = models.BooleanField(default=False, verbose_name='본인인증 여부')
    user_signup_ip = models.CharField(max_length=20, verbose_name='가입 ip')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Date joined')

    # AbstractBaseUser 를 상속받음으로써 정의해줘야하는 필드
    is_active = models.BooleanField(default=False, verbose_name='활성화 여부')
    is_admin = models.BooleanField(default=False, verbose_name='관리자')

    objects = EduGalaxyUserManager()

    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = ['user_nickname']

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자 리스트'

    def get_full_name(self):
        return self.user_nickname

    def get_short_name(self):
        return self.user_nickname

    def __str__(self):
        return self.user_nickname

    # has_perms, has_module_perms 장고 인증 백엔드에서 사용
    # 사용자 특정 권한 여부
    def has_perm(self, perm, obj=None):
        return True

    # user 가 주어진 앱에 해당 권한이 있는지 확인
    def has_module_perms(self, app_label):
        return True

    # 관리자 여부
    @property
    def is_staff(self):
        return self.is_admin

