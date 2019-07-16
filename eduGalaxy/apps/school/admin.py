from apps.school.models import SchoolInfo, SchoolCsvFile
from django import forms
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
import csv


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = SchoolCsvFile
        fields = ('file', 'title')

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = True


class SaveCSVForm(forms.Form):

    csv_dint = SchoolCsvFile.objects.filter().values('id', 'file').order_by('file')

    print(csv_dint)

    select_file = [
        ["dafault", "파일 선택"]
    ]

    for csv_list in csv_dint:
        csv_file = csv_list['file']
        select_file.append([csv_list['file'], csv_file[16:]])

    csv_select = forms.CharField(
        widget=forms.Select(
            choices=tuple(select_file),
            attrs={'id': 'Select_file'},
        ),
        label="CSV 파일 리스트"
    )


class SchoolCsvFileAdmin(admin.ModelAdmin):
    change_list_template = 'admin/CSVFile_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
            path("save-csv/", self.save_csv)
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                self.message_user(request, "csv 저장 완료")
                return redirect("..")
        else:
            form = UploadFileForm()
        return render(request, "admin/csv_import.html", {'form': form})

    def save_csv(self, request):
        if request.method == "POST":
            form = SaveCSVForm(request.POST)
            file = 'media/'
            if form.is_valid():
                file_name = form.cleaned_data["csv_select"]
                file = file + file_name
                with open(file, encoding='euc-kr') as f:
                    reader = csv.reader(f, delimiter=',')
                    for row in reader:
                        print(row[0])
                return redirect("..")
        else:
            form = SaveCSVForm()
        return render(request, "admin/csv_list.html", {'form': form})


# class SchoolInfoAdmin(admin.ModelAdmin):
#     # change_list_template = "admin/schoolInfo_changelist.html"
    #
    # def get_urls(self):
    #     urls = super().get_urls()
    #     my_urls = [

    #
    # def import_csv(self, request):
    #
    #     if request.method == "POST":
    #         # school = SchoolInfo()
    #
    #         file_csv = request.FILES["csv_file"]
    #         csv_data = file_csv.read().decode('euc-kr')
    #         csv_list = csv_data.split('\n')
    #
    #         for line in csv_list:
    #             i = 0
    #             data_list = line.split(',')
    #             for data in data_list:
    #                 print(data + "\n")
    #             i += 1
    #

            # with open(decoded_file,'r', encoding='utf-8') as csvfile:
            #     rr = csv.reader(csvfile, delimiter=",")
            #     for row in rr:
            #         print(row)
            # records = csv.reader(open(file_csv, encoding="utf-8"))

            # for line in records:

                # school.sch_ooe = line[0]
                # school.sch_lea = line[1]
                # school.sch_location = line[2]
                #
                # school.sch_code = line[3]
                # school.sch_name = line[4]
                # school.sch_grade_code = line[5]
                #
                # school.sch_estab_div = line[6]
                # school.sch_char = line[7]
                # school.sch_has_branches = line[8]
                #
                # school.sch_estab_type = line[9]
                # school.sch_day_n_night = line[10]
                # school.sch_anniversary = line[11]
                #
                # school.sch_estab_date = line[12]
                # school.sch_dong_code = line[13]
                # school.sch_address1 = line[14]
                #
                # school.sch_address2 = line[15]
                # school.sch_zip_code = line[16]
                # school.sch_zip_code_st = line[17]
                #
                # school.sch_address1_st = line[18]
                # school.sch_address2_st = line[19]
                # school.sch_lat = line[20]
                #
                # school.sch_lng = line[21]
                # school.sch_phone = line[22]
                # school.sch_fax = line[23]
                #
                # school.sch_homepage = line[24]
                # school.sch_gonghak = line[25]
                #
                # school.save()

admin.site.register(SchoolCsvFile, SchoolCsvFileAdmin)
admin.site.register(SchoolInfo)

