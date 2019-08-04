from apps.school.models import SchoolCsvFile, SchoolInfo
from django import forms
from .models import AdminPost


class SaveCSVForm(forms.Form):

    csv_dint = SchoolCsvFile.objects.filter().values('id', 'file').order_by('file')

    select_file = [
        [0, "파일 선택"]
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


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = SchoolCsvFile
        fields = ('file', 'file_use')

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = True


# class AdminPostForm(forms.ModelForm):
#
#     class Meta:
#         model = AdminPost
#         fields = ()
