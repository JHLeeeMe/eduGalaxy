from apps.school.models import SchoolInfo, SchoolCsvFile
from django import forms
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages

import csv
import os


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = SchoolCsvFile
        fields = ('file', 'file_use')

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = True


class SaveCSVForm(forms.Form):

    csv_dint = SchoolCsvFile.objects.filter().values('id', 'file').order_by('file')

    select_file = [
        ["default", "파일 선택"]
    ]

    for csv_list in csv_dint:
        csv_file = csv_list['file']
        select_file.append([csv_list['id'], csv_file[16:]])

    csv_select = forms.CharField(
        widget=forms.Select(
            choices=tuple(select_file),
            attrs={'id': 'csv_select'}
        ),
        label="CSV 파일 리스트"
    )

    def save(self, row, commit=True):
        school = SchoolInfo()
        school.sch_ooe = row[0]
        school.sch_lea = row[1]
        school.sch_location = row[2]

        school.sch_code = row[3]
        school.sch_name = row[4]
        school.sch_grade_code = int(row[5])

        school.sch_estab_div = row[6]
        school.sch_char = row[7]

        if row[8] == 'Y':
            school.sch_has_branches = True
        else:
            school.sch_has_branches = False

        school.sch_estab_type = row[9]
        school.sch_day_n_night = row[10]
        school.sch_anniversary = row[11]

        school.sch_estab_date = row[12]
        school.sch_dong_code = row[13]
        school.sch_address1 = row[14]

        school.sch_address2 = row[15]
        school.sch_zip_code = row[16]
        school.sch_zip_code_st = row[17]

        school.sch_address1_st = row[18]
        school.sch_address2_st = row[19]
        school.sch_lat = float(row[20])

        school.sch_lng = float(row[21])
        school.sch_phone = row[22]
        school.sch_fax = row[23]

        school.sch_homepage = row[24]
        school.sch_gonghak = row[25]

        if commit:
            school.save()
        return school


class SchoolCsvFileAdmin(admin.ModelAdmin):
    change_list_template = 'admin/CSVFile_change_list.html'

    list_display = (
        'id',
        'file_name',
        'file_use',
    )
    list_display_links = ['id', 'file_name']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
            path("manage-csv/", self.manage_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            uploadFile = request.FILES['file']
            if form.is_valid():
                csv_file = form.save(commit=False)
                csv_file.file_name = uploadFile.name
                csv_file.save()
                self.message_user(request, "csv 저장 완료")

                return redirect("..")
        else:
            form = UploadFileForm()
        return render(request, "admin/csv_import.html", {'form': form})

    def manage_csv(self, request):
        if request.method == "POST":
            form = SaveCSVForm(request.POST)
            file = 'media/'
            if form.is_valid():
                file_id = form.cleaned_data['csv_select']
                file_name = SchoolCsvFile.objects.filter(pk=file_id).values_list('file', flat=True)
                file = file + file_name[0]

                if file_id == "default":
                    messages.error(request, "파일을 선택하세요")
                    form = SaveCSVForm()
                    return render(request, "admin/csv_list.html", {'form': form})

                if 'save' in request.POST:
                    with open(file, encoding='euc-kr') as f:
                        reader = csv.reader(f, delimiter=',')
                        con = 0
                        for row in reader:
                            if con > 0:
                                school = form.save(row, commit=False)
                                school.published_date = timezone.now()
                                school.save()
                            con += 1
                    self.message_user(request, "school DB 저장완료")
                    return redirect("..")
                elif 'delete' in request.POST:
                    csv_file = SchoolCsvFile(pk=file_id)
                    csv_file.delete()
                    if os.path.isfile(file):
                        os.remove(file)
                    self.message_user(request, "해당 파일 삭제")
                    return redirect("..")
        else:
            form = SaveCSVForm()
        return render(request, "admin/csv_list.html", {'form': form})


admin.site.register(SchoolCsvFile, SchoolCsvFileAdmin)
admin.site.register(SchoolInfo)

