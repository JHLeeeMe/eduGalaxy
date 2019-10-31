from django.db import models
from django.utils import timezone

from apps.user.models import EdUser


class Info(models.Model):

    ooe = models.CharField(verbose_name='시도교육청', max_length=30)
    lea = models.CharField(verbose_name='지역교육청', max_length=20, null=True)
    location = models.CharField(verbose_name='지역', max_length=20, null=True)
    scode = models.CharField(verbose_name='정보공시 학교코드', max_length=20)
    name = models.CharField(verbose_name='학교명', max_length=20, null=False)
    gcode = models.IntegerField(default=0, verbose_name='학교급코드', null=False)
    estab_div = models.CharField(verbose_name='설립구분', max_length=4, null=False)
    char = models.CharField(verbose_name='학교특성', max_length=15, null=True)
    has_branches = models.BooleanField(
        verbose_name='분교여부',
        default=False,
        null=True)
    estab_type = models.CharField(verbose_name='설립유형', max_length=4, null=False)
    day_n_night = models.CharField(verbose_name='주야구분', max_length=4, null=False)
    anniversary = models.CharField(verbose_name='개교기념일', max_length=8, null=False)
    estab_date = models.CharField(verbose_name='설립일', max_length=8, null=False)
    dcode = models.CharField(verbose_name='법정동코드', max_length=10, null=False)
    address1 = models.CharField(verbose_name='주소', max_length=40, null=False)
    address2 = models.CharField(verbose_name='상세주소', max_length=25)
    zip_code = models.CharField(verbose_name='우편번호', max_length=6)
    zip_code_st = models.CharField(verbose_name='도로명 우편번호', max_length=5)
    address1_st = models.CharField(verbose_name='도로명주소', max_length=40, null=False)
    address2_st = models.CharField(verbose_name='도로명 상세주소', max_length=25)
    lat = models.FloatField(default=0, verbose_name='위도')
    lng = models.FloatField(default=0, verbose_name='경도')
    tel = models.CharField(verbose_name='전화번호', max_length=20)
    fax = models.CharField(verbose_name='팩스번호', max_length=20, null=True)
    homepage = models.CharField(verbose_name='홈페이지주소', max_length=40, null=True)
    gender_div = models.CharField(verbose_name='남녀공학 구분', max_length=10, null=False)

    num_student = models.IntegerField(default=0, verbose_name='학생 수')
    num_teacher = models.IntegerField(default=0, verbose_name='교직원 수')

    modified_date = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name='수정날짜')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '학교'
        verbose_name_plural = '학교 목록'


class CsvFile(models.Model):
    file = models.FileField(
        null=True,
        verbose_name='파일 경로',
        upload_to="admin/schoolCSV",
    )
    file_use = models.CharField(default='', verbose_name='파일 용도', max_length=25)
    file_name = models.CharField(default='', verbose_name='파일명', max_length=25)

    created_date = models.DateTimeField(default=timezone.now, verbose_name='파일 생성 날짜')
    admin = models.ForeignKey(EdUser, on_delete=models.CASCADE, verbose_name='관리자명')

    class Meta:
        verbose_name = '학교 csv 파일'
        verbose_name_plural = '학교 csv파일 목록'

    def __str__(self):
        return self.file_name


# 학교 관계자 게시판
class Post(models.Model):
    logo = models.CharField(verbose_name='학교로고 파일명', max_length=100, null=True)
    created_date = models.DateTimeField(verbose_name='생성날짜', default=timezone.now)
    modified_date = models.DateTimeField(verbose_name='수정날짜', blank=True, null=True)
    modified_ip = models.CharField(verbose_name='게시판 수정 ip', max_length=20)

    eduser = models.ForeignKey(EdUser, on_delete=models.CASCADE)
    info = models.OneToOneField(Info, on_delete=models.CASCADE)

    def __str__(self):
        return self.info.name


# 사용자 리뷰
class Review(models.Model):
    title = models.CharField(verbose_name='제목', max_length=20)
    content = models.TextField(verbose_name='내용')
    created_date = models.DateTimeField(verbose_name='생성날짜', default=timezone.now)
    created_ip = models.CharField(verbose_name='게시판 생성 ip', max_length=20)

    modified_date = models.DateTimeField(verbose_name='수정날짜', blank=True, null=True)
    modified_ip = models.CharField(verbose_name='게시판 수정 ip', max_length=20)

    eduser = models.ForeignKey(EdUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


