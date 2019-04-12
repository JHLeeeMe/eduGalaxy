from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, View
from django.views.generic.base import TemplateView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, login
from django.contrib import messages

# social auth
from user.oauth.providers.naver import NaverLoginMixin
from django.middleware.csrf import _compare_salted_tokens

from .mixins import VerificationEmailMixin
from .forms import EduGalaxyUserCreationForm


class EduGalaxyUserCreateView(CreateView, VerificationEmailMixin):
    template_name = 'registration/signup.html'
    form_class = EduGalaxyUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance:
            self.send_verification_email(form.instance)
        return response


class EduGalaxyUserVerificationView(TemplateView):
    model = get_user_model()
    token_generator = default_token_generator

    def get(self, request, *args, **kwargs):
        if self.is_valid_token(**kwargs):
            messages.info(request, '인증이 완료되었습니다.')
        else:
            messages.info(request, '인증이 실패되었습니다.')

        return HttpResponseRedirect(reverse('login'))  # 인증 여부와 상관 없이 무조건 로그인 페이지로 이동

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

        return HttpResponseRedirect(reverse('eduGalaxy:index'))


class SocialLoginCallbackView(NaverLoginMixin, View):

    success_url = reverse_lazy('eduGalaxy:index')
    failure_url = reverse_lazy('login')
    required_profiles = ['email', 'gender']
    model = get_user_model()
    oauth_user_id = None

    def get(self, request, *args, **kwargs):

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
            return HttpResponseRedirect(self.success_url)

        return HttpResponseRedirect(self.failure_url)

    def post(self, request, *args, **kwargs):
        self.oauth_user_id = request.POST.get('id')
        SocialLoginCallbackView.get(self, request, *args, **kwargs)
        is_success = request.user.is_authenticated
        return HttpResponseRedirect(self.success_url if is_success else self.failure_url)

    def set_session(self, **kwargs):
        for key, value in kwargs.items():
            self.request.session[key] = value
