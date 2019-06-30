from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import EduGalaxyUser


class EduGalaxyUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = EduGalaxyUser
        fields = ('user_email', 'user_nickname')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호 오류입니다.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user


class EduGalaxyUserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = EduGalaxyUser
        fields = ('user_email', 'password', 'user_nickname', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial['password']


class EduGalaxyUserAdmin(BaseUserAdmin):
    form = EduGalaxyUserChangeForm
    add_form = EduGalaxyUserCreationForm

    list_display =(
        'id',
        'user_email',
        'password',
        'user_nickname',
        'user_age',
        'user_job',
        'user_gender',
        'user_address1',
        'user_address2',
        'user_phone',
        'last_login',
        'user_receive_email',
        'user_confirm',
        'user_signup_ip',
        'date_joined',
        'is_active',
        'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('user_email', 'password','user_nickname')}),
        ('관리자 여부', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_email', 'user_nickname', 'password1', 'password2')}
         ),
    )

    search_fields = ('user_email',)
    ordering = ('date_joined',)
    filter_horizontal = ()


admin.site.register(EduGalaxyUser, EduGalaxyUserAdmin)
admin.site.unregister(Group)

# 주소명 DB 관리(현 보류)

# class DeveloperSite(admin.AdminSite):
#     site_header = "EduGalaxy Developers.."
#     site_title = "EduGalaxy 개발자 사이트 / 안전제일..."
#     index_title = "Good Luck.."
#
#
# class DeveloperInline(admin.StackedInline):
#     model = AddressSelect
#
#
# developer_site = DeveloperSite(name='dev')
#
#
# class AddressSelectAdmin(admin.ModelAdmin):
#     list_display = ['id', 'province', 'city', 'dong']
#     list_per_page = 15
#     list_filter = ['province', 'city']
#
#     ordering = ('province',)
#     filter_horizontal = ()
#
#
# developer_site.register(AddressSelect, AddressSelectAdmin)
