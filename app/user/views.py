from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import FormView, View
from django.views.generic.base import TemplateView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, login
from django.contrib import messages

# social auth
from user.oauth.providers.naver import NaverLoginMixin
from django.middleware.csrf import _compare_salted_tokens

from .mixins import VerificationEmailMixin
from .forms import EduGalaxyUserCreationForm


class EduGalaxyUserCreateView(FormView, VerificationEmailMixin):
    form_class = EduGalaxyUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('user:login')

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
        user = form.save(commit=False)
        user.user_signup_ip = self.request.META['REMOTE_ADDR']
        user.set_password(form.cleaned_data["password1"])
        # response = super(self.form_class, self).form_valid(form)

        user.save()
        self.send_verification_email(user)
        return HttpResponseRedirect(self.get_success_url())

    # def form_valid(self, form):
    '''
        class ModelFormMixin(FormMixin, SingleObjectMixin)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def form_valid(self, form):
            """If the form is valid, save the associated model."""
            self.object = form.save()
            return super().form_valid(form)
        request.POST 값이 들어있는 form(POST값을 머금은 EduGalaxyUser)을 save()함
        
        여기서 super().form_valid(form)은 
        FormMixin에서 
        def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
            return HttpResponseRedirect(self.get_success_url())
        이렇게 정의 돼있음
        
        즉, ModelFormMixin을 상속받는 CreateView를 상속받지 않았으므로 request.POST를 모델에 저장하는 코드 필요.
        
        form.instance는 
        modelFormMixin에서 get_form_kwargs()메서드를 정의할 때 
        'instance'라는 이름으로 self.object(form_valid메서드에서의 그 것)를 딕셔너리(쿼리셋)형태로 집어넣고 리턴해줌
        get_form_kwargs()메서드는 FormMixin의 get_form() 메서드에서 쓰임   
        def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())
        리턴값을 우리 코드로 다시 써보면 EduGalaxyUser({'instance': self.object, ...})
        ModelFormMixin에서 타고타고 올라가다보면 
        BaseForm에 __init__메서드(생성자) 파라미터 여러 개 중에 하나가 instance인걸로 봐선
        어딘가에서 쿼리셋을 키값의 이름을 가진 변수에 밸류값을 넣는 코드가 있을 것으로 판단됨.
        
        결론은 form.instance는 form.save() -> user.save() 이다.
    '''
    #     response = super().form_valid(form)  # response == HttpResponseRedirect(self.get_success_url())
    #     if form.instance:
    #         self.send_verification_email(form.instance)
    #     return response

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class EduGalaxyUserVerificationView(TemplateView):
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

        return HttpResponseRedirect(reverse('eduGalaxy:index'))


class SocialLoginCallbackView(NaverLoginMixin, View):

    success_url = reverse_lazy('eduGalaxy:index')
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


