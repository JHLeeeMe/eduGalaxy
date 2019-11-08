from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render

from config import settings


class VerificationEmailMixin:
    email_template_name = 'user/verification.html'
    token_generator = default_token_generator

    def send_verification_email(self, user):
        token = self.token_generator.make_token(user)
        url = self.build_verification_link(user, token)
        subject = '회원가입을 축하드립니다.'
        message = '다음 주소로 이동하셔서 인증하세요. {}'.format(url)
        html_message = render(self.request, self.email_template_name, {'url': url}).content.decode('utf-8')
        user.email_user(subject, message, from_email=settings.EMAIL_HOST_USER, html_message=html_message)
        messages.info(self.request, '회원가입을 축하드립니다. '
                                    '가입하신 이메일주소로 인증메일을 발송했으니 확인 후 인증해주세요.',
                      extra_tags='send_email_info')

    def build_verification_link(self, user, token):
        # return '{}/user/{}/verify/{}/'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, token)
        return '{}/user/{}/verify/{}/'.format('http://localhost:8000', user.pk, token)
