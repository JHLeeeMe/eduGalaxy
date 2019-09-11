from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView, View, UpdateView
from django.views.generic.base import TemplateView, RedirectView
from django.core.files.storage import FileSystemStorage

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, login
from django.contrib import messages
from django.utils import timezone

# social auth
from .oauth.providers.naver import NaverLoginMixin
from django.middleware.csrf import _compare_salted_tokens

from .mixins import VerificationEmailMixin
from apps.user.forms import EdUserCreationForm, ProfileCreationForm, StudentCreationForm, SchoolAuthCreationForm, PasswordChangeForm
from apps.user.forms import ProfileUpdateForm
from apps.user.models import EdUser, Temp, Profile, Student, SchoolAuth

import os


# 회원가입
class EdUserCreateView(FormView):
    form_class = EdUserCreationForm
    template_name = 'user/create_user.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        temp = form.save(commit=False)
        temp.create_date = timezone.now()
        temp.save()
        eduser_id = temp.id
        return HttpResponseRedirect(reverse_lazy('user:profile', kwargs={'pk': eduser_id}))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ProfileCreateView(FormView):
    form_class = ProfileCreationForm
    template_name = 'user/create_profile.html'

    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(Temp, id=pk)

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name, self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        temp = self.get_object()
        if 'next' in self.request.POST:
            data = form.profile_data()
            group = self.request.POST['group']
            pk = temp.id

            if group == "학생":
                nexturl = 'user:student'
            elif group == "학교 관계자":
                nexturl = 'user:school_auth'
            else:
                return render(self.request, self.template_name, {
                    'error_message': "직업을 선택해주세요",
                })
            temp.profile = data
            temp.create_date = timezone.now()
            temp.save()

            return HttpResponseRedirect(reverse_lazy(nexturl, kwargs={'pk': pk}))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class StudentCreateView(FormView):
    form_class = StudentCreationForm
    template_name = "user/create_student.html"
    success_url = 'user:result'

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name, self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        temp = TempUtil(self.kwargs['pk'])
        temp_object = temp.get_object()

        # EdUer save
        eduser = temp.eduser_save()

        # Profile save
        profile = temp.profile_save()

        # Student save
        student = form.student_data(profile)
        student.gender = self.request.POST.get('gender')  # gender값은 StudentCreationForm에 없고, html에서 넘어옴 for radio btn
        student.save()

        # Temp delete
        temp_object.delete()

        return HttpResponseRedirect(reverse_lazy(self.get_success_url(), kwargs={'pk': eduser.id}))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class SchoolAuthCreateView(FormView):
    form_class = SchoolAuthCreationForm
    template_name = "user/create_school_auth.html"
    success_url = 'user:result'

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name, self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        temp = TempUtil(self.kwargs['pk'])

        # EdUer save
        eduser = temp.eduser_save()

        # Profile save
        profile = temp.profile_save()

        # SchoolAuth save
        school = form.school_auth_data(profile)
        school.save()

        # Temp delete
        temp_object = temp.get_object()
        temp_object.delete()

        return HttpResponseRedirect(reverse_lazy(self.get_success_url(), kwargs={'pk': eduser.id}))


class TempUtil:
    def __init__(self, pk):
        self.temp = get_object_or_404(Temp, id=pk)

    def get_object(self):
        return self.temp

    def eduser_save(self):
        eduser_data = self.temp.eduser.split('| ')
        # EdUser
        self.eduser = EdUser(email=eduser_data[0],
                             password=eduser_data[1],
                             nickname=eduser_data[2])
        self.eduser.save()
        return self.eduser

    def profile_save(self):
        profile_data = self.temp.profile.split('| ')
        # Profile
        profile = Profile(eduser=self.eduser,
                          group=profile_data[0],
                          phone=profile_data[1],
                          receive_email=profile_data[2])
        profile.save()
        return profile


class ResultCreateView(TemplateView):
    template_name = 'user/create_result.html'

    def get(self, request, *args, **kwargs):
        eduser = get_object_or_404(EdUser, id=kwargs['pk'])

        return render(request, self.template_name, {'eduser': eduser})


class TempDeleteView(RedirectView):
    def get(self, request, *args, **kwargs):
        temp = TempUtil(self.kwargs['pk'])
        temp_object = temp.get_object()
        temp_object.delete()
        return redirect('school:index')


# 여기서부터 마이페이지
class EdUserMypageView(TemplateView, LoginRequiredMixin):
    template_name = "user/mypage/index.html"

    def get(self, request, *args, **kwargs):
        email = self.request.user.get_username()
        eduser = EdUser.objects.get(email=email)
        pk = eduser.id
        kwargs.update({'pk': pk})
        return super().get(request, *args, **kwargs)


class PasswordChangeView(FormView, LoginRequiredMixin):
    form_class = PasswordChangeForm
    template_name = "user/mypage/change_password.html"
    success_url = reverse_lazy('user:login')

    def get_object(self):
        email = self.request.user.get_username()
        return get_object_or_404(EdUser, email=email)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        eduser = self.get_object()
        form.user_update(eduser)
        return HttpResponseRedirect(self.get_success_url())


class ProfileUpdateView(UpdateView, LoginRequiredMixin):
    model = Profile
    context_object_name = 'profile'
    form_class = ProfileUpdateForm
    template_name = "user/mypage/update_profile.html"
    success_url = reverse_lazy('user:mypage')

    def get_initial(self):
        group = self.get_group_num()
        if group == 0:
            student = self.get_student()
            self.initial = {
                'school': student.school,
                'grade': student.grade,
                'age': student.age,
                'address1': student.address1,
                'address2': student.address2,
            }
        else:
            schoolauth = self.get_schoolauth()
            self.initial = {
                'school': schoolauth.school,
                'auth_doc': schoolauth.auth_doc,
                'tel': schoolauth.tel,
            }
        return super().get_initial()

    def get_group_num(self):
        profile = self.get_object(queryset=None)
        if profile.group == "학생":
            num = 0
        elif profile.group == "학교 관계자":
            num = 1
        return num

    def get_file(self):
        pk = self.kwargs['pk']
        file = SchoolAuth.objects.filter(profile_id=pk).values_list('auth_doc', flat=True)
        return file

    def get_student(self):
        pk = self.kwargs['pk']
        return get_object_or_404(Student, profile_id=pk)

    def get_schoolauth(self):
        pk = self.kwargs['pk']
        return get_object_or_404(SchoolAuth, profile_id=pk)

    def get_context_data(self, **kwargs):
        kwargs.update({'group': self.get_group_num()})
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        print(form)
        super().get(request, *args, **kwargs)

    def form_valid(self, form):
        group = self.get_group_num()
        if group == 0:
            student = self.get_student()
            form.student_save(student)
        elif group == 1:
            schoolauth = self.get_schoolauth()
            file = self.get_file()
            file_path = "media/" + file[0]

            if os.path.isfile(file_path):
                os.remove(file_path)

            data = form.schoolauth_save(schoolauth)
            data.auth_doc = self.request.FILES['auth_doc']
            data.save()

        return super().form_valid(form)


# 회원 탈퇴 뷰
class EdUserDeleteView(RedirectView, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        eduser = get_object_or_404(EdUser, id=kwargs['pk'])
        eduser.delete()
        return redirect('school:index')


# 여기서부터 소셜 로그인
class EduUserVerificationView(TemplateView):
    model = get_user_model()
    token_generator = default_token_generator

    def get(self, request, *args, **kwargs):
        if self.is_valid_token(**kwargs):
            messages.info(request, '인증이 완료되었습니다.')
        else:
            messages.info(request, '인증이 실패하였습니다.')

        return HttpResponseRedirect(reverse('user:login'))  # 인증 여부와 상관 없이 무조건 로그인 페이지로 이동

    def is_valid_token(self, **kwargs):
        pk = kwargs.get('pk')
        token = kwargs.get('token')
        user = self.model.objects.get(pk=pk)
        is_valid = self.token_generator.check_token(user, token)
        if is_valid:
            user.user_confirm = True
            user.save()
        return is_valid


class ResendVerificationEmailView(View, VerificationEmailMixin):
    model = get_user_model()

    def get(self, request):
        if request.user.is_authenticated and not request.user.user_confirm:
            try:
                user = self.model.objects.get(user_email=request.user.user_email)
            except self.model.DoesNotExist:
                messages.error(self.request, '알 수 없는 사용자 입니다.')
            else:
                self.send_verification_email(user)

        return HttpResponseRedirect(reverse('school:index'))


class SocialLoginCallbackView(NaverLoginMixin, View):

    success_url = reverse_lazy('school:index')
    failure_url = reverse_lazy('user:login')
    required_profiles = ['email', 'gender']
    model = get_user_model()
    oauth_user_id = None

    def get(self, request, **kwargs):

        provider = kwargs.get('provider')
        success_url = request.GET.get('next', self.success_url)

        if provider == 'naver':  # 프로바이더가 naver 일 경우
            csrf_token = request.GET.get('state')
            code = request.GET.get('code')
            if not _compare_salted_tokens(csrf_token, request.COOKIES.get('csrftoken')):  # state(csrf_token)이 잘못된 경우
                messages.error(request, '잘못된 경로로 로그인하셨습니다.', extra_tags='danger')
                return HttpResponseRedirect(self.failure_url)
            is_success, error = self.login_with_naver(csrf_token, code)
            if not is_success:  # 로그인 실패할 경우
                messages.error(request, error, extra_tags='danger')
            return HttpResponseRedirect(success_url if is_success else self.failure_url)

        elif provider == 'google':
            user, created = self.model.objects.get_or_create(user_email=self.oauth_user_id + '@google.comm')
            if created:  # 사용자 생성할 경우
                user.set_password(None)
                user.user_nickname = self.oauth_user_id
                user.user_confirm = True
                user.save()
            return login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        elif provider == 'kakao':
            user, created = self.model.objects.get_or_create(user_email=self.oauth_user_id + '@kakao.comm')
            if created:
                user.set_password(None)
                user.user_nickname = self.oauth_user_id
                user.user_confirm = True
                user.save()
            return login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        return HttpResponseRedirect(self.failure_url)

    def post(self, request, *args, **kwargs):
        self.oauth_user_id = request.POST.get('id')
        SocialLoginCallbackView.get(self, request, *args, **kwargs)
        is_success = request.user.is_authenticated
        return HttpResponseRedirect(self.success_url if is_success else self.failure_url)

    def set_session(self, **kwargs):
        for key, value in kwargs.items():
            self.request.session[key] = value

# self.send_verification_email(user)
#     response = super().form_valid(form)  # response == HttpResponseRedirect(self.get_success_url())
#     if form.instance:
#         self.send_verification_email(form.instance)
#     return response

