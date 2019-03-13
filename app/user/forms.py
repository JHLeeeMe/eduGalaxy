from .models import EduGalaxyUser
from django.contrib.auth.forms import UserCreationForm


class EduGalaxyUserCreationForm(UserCreationForm):

    class Meta:
        model = EduGalaxyUser
        fields = ['user_email',
                  'password1',
                  'password2',
                  'user_nickname',
                  'user_age',
                  'user_job',
                  'user_sex',
                  'user_address1',
                  'user_address2',
                  'user_phone',
                  'user_receive_email',
                  ]

