from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from user import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('eduGalaxy.urls')),
    path('user/login/', views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('user/logout/', views.LogoutView.as_view(template_name='eduGalaxy/index.html'), name='logout'),
    path('user/signup/', user_views.EduGalaxyUserCreateView.as_view(), name='signup'),
    path('user/<pk>/verify/<token>/', user_views.EduGalaxyUserVerificationView.as_view(), name='verify'),
    path('user/resend_verify_email/', user_views.ResendVerificationEmailView.as_view(), name='resend'),
]

