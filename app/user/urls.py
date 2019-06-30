from django.urls import path
from django.contrib.auth import views
from user import views as user_views

app_name = 'user'

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(template_name='eduGalaxy/index.html'), name='logout'),
    path('signup/', user_views.EduGalaxyUserCreateView.as_view(), name='signup'),
    path('<pk>/verify/<token>/', user_views.EduGalaxyUserVerificationView.as_view(), name='verify'),
    path('resend_verify_email/', user_views.ResendVerificationEmailView.as_view(), name='resend'),
    path('login/social/<provider>/callback/', user_views.SocialLoginCallbackView.as_view(), name='social_callback'),
]

