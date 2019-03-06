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

    list_display = ('user_email', 'user_nickname', 'date_joined', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('user_email', 'password','user_nickname')}),
        ('관리자 여부', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':('user_email', 'user_nickname', 'password1', 'password2')}
         ),
    )

    search_fields = ('user_email',)
    ordering = ('date_joined',)
    filter_horizontal = ()


admin.site.register(EduGalaxyUser, EduGalaxyUserAdmin)
admin.site.unregister(Group)