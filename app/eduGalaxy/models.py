from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils import timezone


class EduGalaxyUserManager(BaseUserManager):

    def create_user(self, user_email, user_nickname, password=None):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not user_email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            user_email=self.normalize_email(user_email),
            user_nickname=user_nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_email, user_nickname, password):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다.
        """
        user = self.create_user(
            user_email=user_email,
            password=password,
            user_nickname=user_nickname,
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user

    # def create_user(self, user_email, password):
    #     """
    #     일반 유저 생성
    #     """
    #     return self._create_user(user_email, password, **kwargs)
    #
    # def create_superuser(self, user_email, password):
    #     """
    #     관리자 유저 생성
    #     """
    #     return self._create_user(user_email, password, **kwargs)


class EduGalaxyUser(AbstractBaseUser, PermissionsMixin):
    user_email = models.EmailField(unique=True, max_length=50, verbose_name='이메일')
    user_nickname = models.CharField(unique=True, null=False, max_length=15, verbose_name='닉네임')
    user_age = models.IntegerField(default=28, verbose_name='나이')
    user_job = models.CharField(max_length=30, verbose_name='직업')
    user_sex = models.BooleanField(default=False, verbose_name='성별')
    user_address1 = models.CharField(max_length=100)
    user_address2 = models.CharField(max_length=100)
    user_phone = models.CharField(max_length=15, verbose_name='핸드폰 번호')
    user_receive_email = models.BooleanField(default=False, verbose_name='알림 동의 여부')
    user_confirm = models.BooleanField(default=False, verbose_name='본인인증 여부')
    user_signup_ip = models.CharField(max_length=20, verbose_name='가입 ip')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Date joined')
    is_active = models.BooleanField(default=True, verbose_name='활성화 여부')
    # is_superuser = models.BooleanField(default=False, verbose_name='관리자 여부')
    # is_staff = models.BooleanField(default=False, verbose_name='관리자 페이지 Access 가능 여부')

    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = ['user_nickname']
    objects = EduGalaxyUserManager()

    class Meta:
        db_table = 'edugalaxyuser'
        verbose_name = '유저'
        verbose_name_plural = '유저들'
        ordering = ('-date_joined',)

    def __str__(self):
        return self.user_email + '|' + self.user_nickname

    def get_full_name(self):
        return self.user_nickname

    def get_short_name(self):
        return self.user_nickname

    @property
    def is_staff(self):
        # "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_superuser

    get_full_name.short_description = ('Full name',)

