import apps.school.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(

            name='SchoolCsvFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='admin/schoolCSV', validators=[apps.school.models.csv_select_validator], verbose_name='파일 경로')),
                ('file_use', models.TextField(default='', verbose_name='파일 용도')),
                ('file_name', models.TextField(default='', verbose_name='파일명')),
            ],
            options={
                'verbose_name_plural': '학교 csv파일 리스트',
                'verbose_name': '학교 csv 파일',
            },
        ),
        migrations.CreateModel(

            name='SchoolInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sch_ooe', models.CharField(max_length=30, verbose_name='시도교육청')),
                ('sch_lea', models.CharField(max_length=20, verbose_name='지역교육청')),
                ('sch_location', models.CharField(max_length=20, verbose_name='지역')),
                ('sch_code', models.CharField(max_length=20, verbose_name='정보공시 학교코드')),
                ('sch_name', models.CharField(max_length=20, verbose_name='학교명')),

                ('sch_grade_code', models.IntegerField(default=0, verbose_name='학교급코드')),

                ('sch_estab_div', models.CharField(max_length=4, verbose_name='설립구분')),
                ('sch_char', models.CharField(max_length=15, verbose_name='학교특성')),
                ('sch_has_branches', models.BooleanField(default=False, verbose_name='분교여부')),
                ('sch_estab_type', models.CharField(max_length=4, verbose_name='설립유형')),
                ('sch_day_n_night', models.CharField(max_length=4, verbose_name='주야구분')),

                ('sch_anniversary', models.CharField(max_length=8, verbose_name='개교기념일')),
                ('sch_estab_date', models.CharField(max_length=8, verbose_name='설립일')),
                ('sch_dong_code', models.CharField(max_length=10, verbose_name='법정동코드')),
                ('sch_address1', models.CharField(max_length=40, verbose_name='주소')),
                ('sch_address2', models.CharField(max_length=25, verbose_name='상세주소')),
                ('sch_zip_code', models.CharField(max_length=6, verbose_name='우편번호')),
                ('sch_zip_code_st', models.CharField(max_length=5, verbose_name='도로명 우편번호')),
                ('sch_address1_st', models.CharField(max_length=40, verbose_name='도로명주소')),
                ('sch_address2_st', models.CharField(max_length=25, verbose_name='도로명 상세주소')),
                ('sch_lat', models.FloatField(default=0, verbose_name='위도')),
                ('sch_lng', models.FloatField(default=0, verbose_name='경도')),


                ('sch_phone', models.CharField(max_length=20, verbose_name='전화번호')),
                ('sch_fax', models.CharField(max_length=20, verbose_name='팩스번호')),
                ('sch_homepage', models.CharField(max_length=40, verbose_name='홈페이지주소')),
                ('sch_gonghak', models.CharField(max_length=10, verbose_name='남녀공학 구분')),

                ('published_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': '학교 리스트',
                'verbose_name': '학교',
            },

        ),
    ]
