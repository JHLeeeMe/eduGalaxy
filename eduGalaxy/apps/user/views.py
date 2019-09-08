from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView, View, UpdateView
from django.views.generic.base import TemplateView, RedirectView

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
    success_url = reverse_lazy('user:login')

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
        gender = self.request.POST['gender']
        data = form.student_data()
        temp = self.get_object()
        student = data['front'] + "| " + gender + "| " + data['back']

        temp.student = student
        temp.create_date = timezone.now()
        temp.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class SchoolAuthCreateView(FormView):
    form_class = SchoolAuthCreationForm
    template_name = "user/create_school_auth.html"
    success_url = reverse_lazy('user:login')

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
        data = form.school_auth_data()

        temp.schoolauth = data
        temp.create_date = timezone.now()
        temp.save()

        print(type(temp.schoolauth[2]))

        return HttpResponseRedirect(self.get_success_url())


#class ResultCreateView(FormView):
#    form_class = ResultCreationForm
#    template_name = 'user/create_result.html'

#    def get_object(self):
#        pk = self.kwargs['pk']
#        return get_object_or_404(Temp, id=pk)

#    def post(self, request, *args, **kwargs):
#        form = self.get_form()
#        if form.is_valid():
#            return self.form_valid(form)
#        else:
#            return self.form_invalid(form)

#    def form_valid(self, form):
#        return HttpResponseRedirect(self.get_success_url())


class TempDeleteView(RedirectView):
    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(Temp, id=pk)

    def get(self, request, *args, **kwargs):
        temp = self.get_object()
        temp.delete()
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
        return super().get_initial()

    def get_group_num(self):
        profile = self.get_object(queryset=None)
        if profile.group == "학생":
            num = 0
        elif profile.group == "학교 관계자":
            num = 1
        return num

    def get_student(self):
        pk = self.kwargs['pk']
        return get_object_or_404(Student, profile_id=pk)

    def get_schoolauth(self):
        pk = self.kwargs['pk']
        return get_object_or_404(SchoolAuth, profile_id=pk)

    def get_context_data(self, **kwargs):
        kwargs.update({'group': self.get_group_num()})
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        student = self.get_student()
        form.student_save(student)
        return super().form_valid(form)


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
#
#


# '''
#     class ModelFormMixin(FormMixin, SingleObjectMixin)
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#         """If the form is valid, save the associated model."""
#         self.object = form.save()
#         return super().form_valid(form)
#     request.POST 값이 들어있는 form(POST값을 머금은 EduUser)을 save()함
#
#     여기서 super().form_valid(form)은
#     FormMixin에서
#     def form_valid(self, form):
#     """If the form is valid, redirect to the supplied URL."""
#         return HttpResponseRedirect(self.get_success_url())
#     이렇게 정의 돼있음
#
#     즉, ModelFormMixin을 상속받는 CreateView를 상속받지 않았으므로 request.POST를 모델에 저장하는 코드 필요.
#
#     form.instance는
#     modelFormMixin에서 get_form_kwargs()메서드를 정의할 때
#     'instance'라는 이름으로 self.object(form_valid메서드에서의 그 것)를 딕셔너리(쿼리셋)형태로 집어넣고 리턴해줌
#     get_form_kwargs()메서드는 FormMixin의 get_form() 메서드에서 쓰임
#     def get_form(self, form_class=None):
#     """Return an instance of the form to be used in this view."""
#     if form_class is None:
#         form_class = self.get_form_class()
#     return form_class(**self.get_form_kwargs())
#     리턴값을 우리 코드로 다시 써보면 EduUser({'instance': self.object, ...})
#     ModelFormMixin에서 타고타고 올라가다보면
#     BaseForm에 __init__메서드(생성자) 파라미터 여러 개 중에 하나가 instance인걸로 봐선
#     어딘가에서 쿼리셋을 키값의 이름을 가진 변수에 밸류값을 넣는 코드가 있을 것으로 판단됨.
#
#     결론은 form.instance는 form.save() -> user.save() 이다.
# '''
#     response = super().form_valid(form)  # response == HttpResponseRedirect(self.get_success_url())
#     if form.instance:
#         self.send_verification_email(form.instance)
#     return response

