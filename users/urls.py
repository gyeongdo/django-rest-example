from users.views import *
from django.conf.urls import url
from django.urls import path, include, re_path

app_name = "users"

urlpatterns = [

    url(r"auth/", include("knox.urls")),
    path('register/', RegistrationAPI.as_view()),

    # url(r'login/', LoginView.as_view(), name='knox_login'),
    # path('login/', LoginAPI.as_view()),

    path('user/', UserAPI.as_view()),
    # path("auth/profile/<int:user_pk>/update/", ProfileUpdateAPI.as_view()),

    path('login/kakao/', Kakao.as_view()),
    path('login/kakao/callback/', KakaoCallback.as_view()),

]
