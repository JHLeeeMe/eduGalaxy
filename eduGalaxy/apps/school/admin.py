from apps.school.models import SchoolInfo
from django import forms
from django.contrib import admin

import csv


class CsvImportForm(forms.ModelForm):
    csv_file = forms.FileField()

    class Meta:
        model = SchoolInfo
        fields = ("csv_file",)

    def save(self, commit=False, *args, **kwargs):
        school = SchoolInfo()

        file_csv = self.cleaned_data['csv_file']
        datafile = open(file_csv, 'rb')
        records = csv.reader(datafile)

        for line in records:
            school.sch_ooe = line[1]
            school.sch_lea = line[2]
            school.sch_location = line[3]

            school.sch_inf_code = line[4]
            school.sch_name = line[5]
            school.sch_grade_code= line[6]

            school.sch_estab_div = line[7]
            school.sch_char = line[8]
            school.sch_has_branches = line[9]

            school.sch_estab_type = line[10]
            school.sch_day_n_night = line[11]
            school.sch_anniversary = line[12]

            school.sch_estab_date = line[10]
            school.sch_dong_code = line[11]
            school.sch_address1 = line[12]

            school.sch_address2 = line[13]
            school.sch_zip_code = line[14]
            school.sch_zip_code_st = line[15]

            school.sch_address1_st = line[16]
            school.sch_address2_st = line[17]
            school.sch_lat = line[18]

            school.sch_lng = line[16]
            school.sch_phone = line[17]
            school.sch_fax = line[18]

            school.sch_homepage = line[16]
            school.sch_gonghak = line[17]

            school.save()

        datafile.close()


class SchoolInfoAdmin(admin.ModelAdmin):
    form = CsvImportForm()


admin.site.register(SchoolInfo, SchoolInfoAdmin)
