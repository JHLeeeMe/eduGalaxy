from apps.school.models import SchoolInfo
from django import forms
from django.contrib import admin

import csv


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

    def save(self):
        school = SchoolInfo()

        file_csv = self.cleaned_data['csv_file']
        datafile = open(file_csv, 'rb')
        records = csv.reader(datafile)

        for line in records:
            school.sch_ooe = line[0]
            school.sch_lea = line[1]
            school.sch_location = line[2]

            school.sch_inf_code = line[3]
            school.sch_name = line[4]
            school.sch_grade_code= line[5]

            school.sch_estab_div = line[6]
            school.sch_char = line[7]
            school.sch_has_branches = line[8]

            school.sch_estab_type = line[9]
            school.sch_day_n_night = line[10]
            school.sch_anniversary = line[11]

            school.sch_estab_date = line[12]
            school.sch_dong_code = line[13]
            school.sch_address1 = line[14]

            school.sch_address2 = line[15]
            school.sch_zip_code = line[16]
            school.sch_zip_code_st = line[17]

            school.sch_address1_st = line[18]
            school.sch_address2_st = line[19]
            school.sch_lat = line[20]

            school.sch_lng = line[21]
            school.sch_phone = line[22]
            school.sch_fax = line[23]

            school.sch_homepage = line[24]
            school.sch_gonghak = line[25]

            school.save()

        datafile.close()


class SchoolInfoAdmin(admin.ModelAdmin):
    change_list_template = "admin/schoolInfo_changelist.html"

    def get_urls(self):



admin.site.register(SchoolInfo, SchoolInfoAdmin)
