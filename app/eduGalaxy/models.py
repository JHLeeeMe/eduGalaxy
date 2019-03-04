from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils import timezone


class EduGalaxyUserManager(BaseUserManager):
    def _create_user(self, user_email, password=None, **kwargs):
        if not user_email:
            raise ValueError('이메일은 필수입니다.')
        user = self.model(user_email=self.normalize_email(user_email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

    def create_user(self, user_email, password, **kwargs):
        """
        일반 유저 생성
        """
        kwargs.setdefault('is_superuser', False)
        return self._create_user(user_email, password, **kwargs)

    def create_superuser(self, user_email, password, **kwargs):
        """
        관리자 유저 생성
        """
        kwargs.setdefault('is_superuser', True)
        return self._create_user(user_email, password, **kwargs)


class EduGalaxyUser(AbstractBaseUser, PermissionsMixin):
    # uuid = models.UUIDField(
    #     primary_key=True,
    #     unique=True,
    #     editable=False,
    #     default=uuid.uuid4,
    #     verbose_name='PK'
    # )
    user_email = models.EmailField(unique=True, max_length=50, verbose_name='아이디')
    user_nickname = models.CharField(max_length=15, verbose_name='닉네임')
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
    is_superuser = models.BooleanField(default=False, verbose_name='관리자 여부')
    is_staff = models.BooleanField(default=False, verbose_name='관리자 페이지 Access 가능 여부')

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

