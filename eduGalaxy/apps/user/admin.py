from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from apps.user.models import EdUser, Profile, SchoolAuth, Student
from apps.user.models import Parent, Child, Log, Temp


class EdUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = EdUser
        fields = ('email', 'nickname')

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


class EdUserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = EdUser
        fields = ('email', 'password', 'nickname', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial['password']


class EdUserAdmin(BaseUserAdmin):
    form = EdUserChangeForm
    add_form = EdUserCreationForm

    list_display =(
        'id',
        'email',
        'nickname',
        'is_active',
        'is_admin')
    list_filter = ('is_admin', 'is_active')
    list_per_page = 15
    list_display_links = ('email', )
    ordering = ('id', )
    fieldsets = (
        (None, {'fields': ('email', 'nickname')}),
        ('계정 관리', {'fields': ('is_admin', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2')}
         ),
    )

    search_fields = ('email',)
    filter_horizontal = ()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_id',
                    'get_email',
                    'group',
                    'receive_email',
                    'confirm')
    list_display_links = ('get_email',)
    list_filter = ('group', )

    list_per_page = 15

    def get_id(self, obj):
        return obj.eduser.id

    def get_email(self, obj):
        return obj.eduser.email

    get_id.short_description = 'ID'
    get_email.short_description = '이메일'
    get_id.admin_order_field = 'eduser'


class SchoolAuthAdmin(admin.ModelAdmin):
    list_display = ('get_id',
                    'get_email',
                    'school',
                    'tel',
                    'get_confirm')
    list_display_links = ('get_email',)
    list_per_page = 15

    def get_id(self, obj):
        return obj.profile.eduser.id

    def get_email(self, obj):
        return obj.profile.eduser.email

    def get_confirm(self, obj):
        return obj.profile.confirm

    get_id.short_description = 'ID'
    get_email.short_description = '이메일'
    get_confirm.short_description = '인증 여부'
    get_id.admin_order_field = 'profile'


class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_id',
                    'get_email',
                    'school',
                    'age')
    list_display_links = ('get_email',)

    list_per_page = 15

    def get_id(self, obj):
        return obj.profile.eduser.id

    def get_email(self, obj):
        return obj.profile.eduser.email

    get_id.short_description = 'ID'
    get_email.short_description = '이메일'
    get_id.admin_order_field = 'profile'


class ParentAdmin(admin.ModelAdmin):
    list_display = ('get_id',
                    'get_email',
                    'address1')
    list_display_links = ('get_email',)

    list_per_page = 15

    def get_id(self, obj):
        return obj.profile.eduser.id

    def get_email(self, obj):
        return obj.profile.eduser.email

    get_id.short_description = 'ID'
    get_email.short_description = '이메일'
    get_id.admin_order_field = 'profile'


class ChildAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'get_email',
                    'school',
                    'age')
    list_display_links = ('get_email',)
    ordering = ('id', )
    list_per_page = 15

    def get_email(self, obj):
        return obj.parent.profile.eduser.email

    get_email.short_description = '이메일'


class LogAdmin(admin.ModelAdmin):
    list_display = ('get_id',
                    'get_email',
                    'signup_ip',
                    'created_date',
                    'login_ip',
                    'get_login_date')
    list_display_links = ('get_email',)

    list_per_page = 15

    def get_id(self, obj):
        return obj.eduser.id

    def get_email(self, obj):
        return obj.eduser.email

    def get_login_date(self, obj):
        return obj.eduser.last_login

    get_id.short_description = 'ID'
    get_email.short_description = '이메일'
    get_id.admin_order_field = 'eduser'
    get_login_date.short_description = '마지막 로그인 날짜'


class TempAdmin(admin.ModelAdmin):
    list_display = ('id', 'eduser', 'profile', 'create_date')
    list_display_links = ('id',)
    list_per_page = 15


admin.site.register(EdUser, EdUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(SchoolAuth, SchoolAuthAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Child, ChildAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Temp, TempAdmin)
admin.site.unregister(Group)


