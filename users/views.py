from .serializers import *
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from . import models

# 회원가입
class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        # if len(request.data["username"]) < 6 or len(request.data["password"]) < 4:
        #     body = {"message": "short field"}
        #     return Response(body, status=status.HTTP_400_BAD_REQUEST)

        print("request.data : ", request.data["profile"])
        print("request.data : ", request.data["profile"]["email"])

        # serializer = self.get_serializer(data=request.data)
        # serializer.set_unusable_password()
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        user = models.User.objects.create(
            username='admin2',
            email='admin2@admin2.com',
        )
        user.set_unusable_password()
        user.save()

        print('3')
        # user = serializer.save()
        print('4')
        # profile을 instance로 넘기는 방법을 몰라서
        # view에서 save로 강제로 저장
        print('user :: ', user)
        profile = Profile(user=user, user_pk=user.id, email=request.data["profile"]["email"])
        profile.save()

        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        # serializer = AuthTokenSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        #
        # user = serializer.validated_data['user']
        user = models.User.objects.get(email='admin2@admin2.com')

        login(request, user)

        return super(LoginView, self).post(request, format=None)

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        user_serializer = UserSerializer(user, context=self.get_serializer_context()).data
        return Response(
            {
                "user": user_serializer,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ProfileUpdateAPI(generics.UpdateAPIView):
    lookup_field = "user_pk"
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


from django.shortcuts import redirect
import urllib

# code 요청
class Kakao(generics.GenericAPIView):
    def get(self, request):
        print('@@@@@@@@ code')
        app_rest_api_key = '11ff6255eaefbf394891fbdb27f66362'
        redirect_uri = "http://127.0.0.1:8000/api/users/login/kakao/callback"

        # return redirect("http://127.0.0.1:8000/api/users/login/kakao/callback")
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code")


# access token 요청
class KakaoCallback(generics.GenericAPIView):
    def get(self, request):
        print('@@@@@@@@ calaback')
        params = urllib.parse.urlencode(request.GET)
        print('@@@@@@@@ access_token', params)
        # # return redirect(f'http://127.0.0.1:8000/api/users/login/kakao/callback?{params}')
        # return redirect("http://127.0.0.1:8080")
        return Response({
            'asdf': 'asd'
        })