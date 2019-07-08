from django.db import models


class SchoolInfo(models.Model):

    sch_ooe = models.CharField(verbose_name='시도교육청')
    sch_lea = models.CharField(verbose_name='지역교육청')
    sch_location = models.CharField(verbose_name='지역')
    sch_code = models.CharField(verbose_name='학교코드')
    sch_name = models.CharField(verbose_name='학교명', null=False)
    sch_grade_code = models.IntegerField(verbose_name='학교급코드', null=False)
    sch_estab_div = models.CharField(verbose_name='설립구분', null=False)
    sch_char = models.CharField(verbose_name='학교특성')
    sch_has_branches = models.BooleanField(
        verbose_name='분교여부',
        default=False,
        null=False)
    sch_estab_type = models.CharField(verbose_name='설립유형', null=False)
    sch_day_n_night = models.CharField(verbose_name='주야구분', null=False)
    sch_anniversary = models.IntegerField(verbose_name='개교기념일', null=False)
    sch_estab_date = models.IntegerField(verbose_name='설립일', null=False)
    sch_dong_code = models.IntegerField(verbose_name='법정동코드', null=False)
    sch_address1 = models.CharField(verbose_name='주소', null=False)
    sch_address2 = models.CharField(verbose_name='상세주소')
    sch_zip_code = models.IntegerField(verbose_name='우편번호')
    sch_address1_st = models.CharField(verbose_name='도로명주소', null=False)
    sch_address2_st = models.CharField(verbose_name='도로명 상세주소')
    sch_zip_code_st = models.IntegerField(verbose_name='도로명 우편번호')
    sch_lat = models.FloatField(verbose_name='위도')
    sch_lng = models.FloatField(verbose_name='경도')
    sch_phone = models.CharField(verbose_name='전화번호')
    sch_fax = models.CharField(verbose_name='팩스번호')
    sch_homepage = models.CharField(verbose_name='홈페이지주소')
    sch_gonghak = models.CharField(verbose_name='남녀공학 구분', null=False)

    def __str__(self):
        return self.sch_name

