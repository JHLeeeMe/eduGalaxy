# from django.db import models
#
#
# class SchoolInfo(models.Model):
#
#     sch_ooe = models.CharField(verbose_name='시도교육청')
#     sch_lea = models.CharField(verbose_name='지역교육청')
#     ######## 바꿔@#########c########
#     # sch_?? = models.CharField(verbose_name='지역')
#     sch_code = models.CharField(verbose_name='학교코드')
#     sch_name = models.CharField(verbose_name='학교명', null=False)
#     sch_grade_code = models.IntegerField(verbose_name='학교급코드', null=False)
#     sch_estab_div = models.CharField(verbose_name='설립구분', null=False)
#     sch_char = models.CharField(verbose_name='학교특성')
#     sch_has_branches = models.BooleanField(
#         verbose_name='분교여부',
#         default=False,
#         null=False)
#     sch_estab_type = models.CharField(verbose_name='설립유형', null=False)
#     sch_day_n_night = models.CharField(verbose_name='주야구분', null=False)
#     sch_anniversary = models.IntegerField(verbose_name='개교기념일', null=False)
#     sch_estab_date = models.IntegerField(verbose_name='설립일', null=False)
#     sch_dong_code = models.IntegerField(verbose_name='법정동코드', null=False)
#     sch_address1 = models.CharField(verbose_name='주소', null=False)
#     sch_address2 = models.CharField(verbose_name='상세주소', null=False)
#     sch_zip_code = models.IntegerField(verbose_name='우편번호', null=False)
#     sch_address1_st = models.CharField(verbose_name='도로명주소', null=False)
#     sch_address2_st = models.CharField(verbose_name='도로명 상세주소', null=False)
#     sch_zip_code_st = models.IntegerField(verbose_name='도로명 우편번호', null=False)
#     sch_lat = models.FloatField(verbose_name='위도')
#     sch_long = models.FloatField(verbose_name='경도')
#     sch_phone = models.CharField(verbose_name='전화번호')
#     sch_fax = models.CharField(verbose_name='팩스번호')
#     sch_homepage = models.CharField(verbose_name='홈페이지주소')
#
#     ######## 바꿔@#################
#     sch_gonghak_classasfd = models.CharField(verbose_name='남녀공학 구분')
#
#


    # user_email = models.EmailField(
    #     unique=True,
    #     max_length=50,
    #     verbose_name='이메일'
    # )
    # user_nickname = models.CharField(
    #     unique=True,
    #     max_length=50,
    #     verbose_name='닉네임',
    #     null=False
    # )
    #
    # # 상세 입력 사항
    # user_age = models.IntegerField(default=0, verbose_name='나이')
    # user_job = models.CharField(max_length=30, verbose_name='직업')
    # user_gender = models.CharField(default='U', max_length=2, verbose_name='성별')
    # user_address1 = models.CharField(max_length=100)
    # user_address2 = models.CharField(max_length=100)
    # user_phone = models.CharField(max_length=15, verbose_name='핸드폰 번호')
    # user_receive_email = models.BooleanField(default=False, verbose_name='알림 동의 여부')
    #
    # # 관리자 필요 데이터
    # user_confirm = models.BooleanField(default=False, verbose_name='본인인증 여부')
    # user_signup_ip = models.CharField(max_length=20, verbose_name='가입 ip')
    # date_joined = models.DateTimeField(default=timezone.now, verbose_name='가입날짜')
    #
    # # AbstractBaseUser 를 상속받음으로써 정의해줘야하는 필드
    # is_active = models.BooleanField(default=True, verbose_name='활성화 여부')
    # is_admin = models.BooleanField(default=False, verbose_name='관리자')
    #
    # objects = EduUserManager()
    #
    # USERNAME_FIELD = 'user_email'
    # REQUIRED_FIELDS = ['user_nickname']
    #
    # class Meta:
    #     verbose_name = '사용자'
    #     verbose_name_plural = '사용자 리스트'
    #
    # def get_full_name(self):
    #     return self.user_nickname
    #
    # def get_short_name(self):
    #     return self.user_nickname
    #
    # def __str__(self):
    #     return self.user_nickname