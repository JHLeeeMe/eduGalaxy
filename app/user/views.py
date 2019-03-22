from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, View
from django.views.generic.base import TemplateView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib import messages

from .mixins import VerificationEmailMixin
from .forms import EduGalaxyUserCreationForm


# class SignInView():
#
# class SignOutView():

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

# class ResendVerificationEmailView(FormView, VerificationEmailMixin):
#     template_name = 'registration/resend_verification.html'
#     model = get_user_model()
#     form_class = VerificationEmailForm
#     success_url = reverse_lazy('login')
#
#     def form_valid(self, form):
#         email = form.cleaned_data['user_email']
#         try:
#             user = self.model.objects.get(user_email=email)
#         except self.model.DoesNotExist:
#             messages.error(self.request, '알 수 없는 사용자 입니다.')
#         else:
#             self.send_verification_email(user)
#         return super().form_valid(form)
