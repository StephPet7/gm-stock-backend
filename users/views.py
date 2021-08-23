import jwt

# Create your views here.
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            user = reg_serializer.save()
            if user:
                return Response(status=status.HTTP_201_CREATED)
            return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        user = User.objects.get(id=request.data['id'])
        data = dict(request.data)
        keys = data.keys()

        for key in keys:
            if key == 'email':
                user.email = data['email'][0]
            if key == 'user_name':
                user.user_name = data['user_name'][0]
            if key == 'name':
                user.name = data['name'][0]
            if key == 'is_active':
                user.is_active = data['is_active'][0]
            if key == 'password':
                user.password = data['password'][0]
            if key == 'role':
                user.role = data['role'][0]

        user.save()
        serializer = RegisterUserSerializer(user)
        return Response(serializer.data)


class AllUsers(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        users = User.objects.all()
        serializer = RegisterUserSerializer(users, many=True)
        return Response(serializer.data)


class RetrieveUser(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(id=request.GET['id'])
        serializer = RegisterUserSerializer(user)
        return Response(serializer.data)


class BlackListTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = TokenObtainPairSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        token_pair = serializer.validated_data
        response = Response()
        response.set_cookie(key="access", value=token_pair['access'], httponly=True)
        response.set_cookie(key="refresh", value=token_pair['refresh'], httponly=True)
        return response


class RetrieveWithToken(APIView):
    def get(self, request):
        token = request.COOKIES.get('access')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['user_id']).first()
        serializer = RegisterUserSerializer(user)
        return Response(serializer.data)
