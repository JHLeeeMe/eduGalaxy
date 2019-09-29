from django.conf import settings
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from apps.user.models import Temp, Profile
import requests


class NaverClient:
    client_id = settings.NAVER_CLIENT_ID
    secret_key = settings.NAVER_SECRET_KEY
    grant_type = 'authorization_code'

    auth_url = 'https://nid.naver.com/oauth2.0/token'
    profile_url = 'https://openapi.naver.com/v1/nid/me'

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def get_access_token(self, state, code):
        res = requests.get(self.auth_url, params={'client_id': self.client_id, 'client_secret': self.secret_key,
                                                  'grant_type': self.grant_type, 'state': state, 'code': code})

        return res.ok, res.json()

    def get_profile(self, access_token, token_type='Bearer'):
        res = requests.get(self.profile_url, headers={'Authorization': '{} {}'.format(token_type, access_token)}).json()

        if not res.get('resultcode') == '00':
            return False, res.get('message')
        else:
            # {
            #   "resultcode": "00",
            #   "message": "success",
            #   "response": {
            #     "email": "openapi@naver.com",
            #     "nickname": "OpenAPI",
            #     "profile_image": "https://ssl.pstatic.net/static/pwe/address/nodata_33x33.gif",
            #     "age": "40-49",
            #     "gender": "F",
            #     "id": "32742776",
            #     "name": "오픈 API",
            #     "birthday": "10-01"
            #   }
            # }
            return True, res.get('response')


class NaverLoginMixin:
    naver_client = NaverClient()

    def login_or_create_with_naver(self, state, code):
        
        # 인증토큰 발급
        is_success, token_infos = self.naver_client.get_access_token(state, code)

        if not is_success:
            return False, '{} [{}]'.format(token_infos.get('error_desc'), token_infos.get('error'))

        access_token = token_infos.get('access_token')
        refresh_token = token_infos.get('refresh_token')
        expires_in = token_infos.get('expires_in')
        token_type = token_infos.get('token_type')

        # 네이버 프로필 얻기
        is_success, profiles = self.get_naver_profile(access_token, token_type)
        if not is_success:
            return False, profiles

        # 세션데이터 추가
        self.set_session(access_token=access_token, refresh_token=refresh_token,
                         expires_in=expires_in, token_type=token_type)

        # 사용자 로그인 or 생성
        try:
            # 유저 검색
            user = self.model.objects.get(email=profiles.get('email'))
            profile = Profile.objects.get(eduser_id=user.id)
            if not profile.is_naver:  # 기존 유저는 있지만 소셜 연동(naver)을 하지 않았을 때
                if profile.confirm:
                    profile.is_naver = True
                    profile.save()
                    login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
                else:
                    data = ['같은 이메일로 가입된 정보가 있습니다. 본인 확인용 메일을 보내드렸습니다. 인증 후 연동 가능합니다.']
                    data.append(reverse_lazy('school:index'))
                    data.append(user)
                    data.append(profile)
                    return False, data
            else:
                login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        except ObjectDoesNotExist:  # EdUser 모델이 없을 경우
            # Temp save
            data = profiles.get('email') + '| ' + 'social_password' + '| ' + 'social_nickname' + '| ' + 'naver'

            temp = Temp(eduser=data)
            temp.create_date = timezone.now()
            temp.save()

            return True, reverse_lazy('user:profile', kwargs={'pk': temp.id})

        return True, reverse_lazy('school:index')

    def get_naver_profile(self, access_token, token_type):
        is_success, profiles = self.naver_client.get_profile(access_token, token_type)

        if not is_success:
            return False, profiles

        for profile in self.required_profiles:
            if profile not in profiles:
                return False, '{}은 필수정보입니다. 정보제공에 동의해주세요.'.format(profile)

        return True, profiles

