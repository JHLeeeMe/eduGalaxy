from django.db import models
from django import forms
from django.utils import timezone

from apps.user.models import EduUser


def csv_select_validator(value):
    if value == "파일 선택":
        raise forms.ValidationError('파일을 선택하세요')


class SchoolInfo(models.Model):

    sch_ooe = models.CharField(verbose_name='시도교육청', max_length=30)
    sch_lea = models.CharField(verbose_name='지역교육청', max_length=20)
    sch_location = models.CharField(verbose_name='지역', max_length=20)
    sch_code = models.CharField(verbose_name='정보공시 학교코드', max_length=20)
    sch_name = models.CharField(verbose_name='학교명', max_length=20, null=False)

    sch_grade_code = models.IntegerField(default=0, verbose_name='학교급코드', null=False)

    sch_estab_div = models.CharField(verbose_name='설립구분', max_length=4, null=False)
    sch_char = models.CharField(verbose_name='학교특성', max_length=15)
    sch_has_branches = models.BooleanField(
        verbose_name='분교여부',
        default=False,
        null=False)
    sch_estab_type = models.CharField(verbose_name='설립유형', max_length=4, null=False)
    sch_day_n_night = models.CharField(verbose_name='주야구분', max_length=4, null=False)

    sch_anniversary = models.CharField(verbose_name='개교기념일', max_length=8, null=False)
    sch_estab_date = models.CharField(verbose_name='설립일', max_length=8, null=False)
    sch_dong_code = models.CharField(verbose_name='법정동코드', max_length=10, null=False)
    sch_address1 = models.CharField(verbose_name='주소', max_length=40, null=False)
    sch_address2 = models.CharField(verbose_name='상세주소', max_length=25)
    sch_zip_code = models.CharField(verbose_name='우편번호', max_length=6)
    sch_zip_code_st = models.CharField(verbose_name='도로명 우편번호', max_length=5)
    sch_address1_st = models.CharField(verbose_name='도로명주소', max_length=40, null=False)
    sch_address2_st = models.CharField(verbose_name='도로명 상세주소', max_length=25)
    sch_lat = models.FloatField(default=0, verbose_name='위도')
    sch_lng = models.FloatField(default=0, verbose_name='경도')
    sch_phone = models.CharField(verbose_name='전화번호', max_length=20)
    sch_fax = models.CharField(verbose_name='팩스번호', max_length=20)
    sch_homepage = models.CharField(verbose_name='홈페이지주소', max_length=40)
    sch_gonghak = models.CharField(verbose_name='남녀공학 구분', max_length=10, null=False)

    published_date = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return self.sch_name


    class Meta:
        verbose_name = '학교'
        verbose_name_plural = '학교 리스트'


class SchoolCsvFile(models.Model):
    file = models.FileField(
        null=False,
        verbose_name='파일 경로',
        upload_to="admin/schoolCSV",
        validators=[csv_select_validator]
    )
    file_use = models.TextField(default='', verbose_name='파일 용도')
    file_name = models.TextField(default='', verbose_name='파일명')

    class Meta:
        verbose_name = '학교 csv 파일'
        verbose_name_plural = '학교 csv파일 리스트'

    def __str__(self):
        return self.file_name



# 학교 관계자 게시판
class AdminPost(models.Model):
    logo = models.CharField(verbose_name='학교로고 파일명', max_length=100)
    created_date = models.DateTimeField(verbose_name='생성날짜', default=timezone.now)
    created_ip = models.CharField(verbose_name='게시판 생성 ip', max_length=20)

    modified_date = models.DateTimeField(verbose_name='수정날짜', blank=True, null=True)
    modified_ip = models.CharField(verbose_name='게시판 수정 ip', max_length=20)

    edu_user = models.ForeignKey(EduUser, on_delete=models.CASCADE)
    school_info = models.ForeignKey(SchoolInfo, on_delete=models.CASCADE)


# 사용자 리뷰
class UserPost(models.Model):
    title = models.CharField(verbose_name='제목', max_length=20)
    content = models.TextField(verbose_name='내용')
    created_date = models.DateTimeField(verbose_name='생성날짜', default=timezone.now)
    created_ip = models.CharField(verbose_name='게시판 생성 ip', max_length=20)

    modified_date = models.DateTimeField(verbose_name='수정날짜', blank=True, null=True)
    modified_ip = models.CharField(verbose_name='게시판 수정 ip', max_length=20)

    edu_user = models.ForeignKey(EduUser, on_delete=models.CASCADE)
    adminPost = models.ForeignKey(AdminPost, on_delete=models.CASCADE)


