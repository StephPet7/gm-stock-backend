
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
                user.email = data['email']
            if key == 'user_name':
                user.user_name = data['user_name']
            if key == 'name':
                user.name = data['name']
            if key == 'is_active':
                user.is_active = data['is_active']
            if key == 'password':
                user.password = data['password']
            if key == 'role':
                user.role = data['role']

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


class RetrieveWithToken(APIView):
    def get(self, request):
        try:
            token = request.headers['Authorization'].split(" ")[1]
        except KeyError:
            raise AuthenticationFailed("Unauthenticated!")
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['user_id']).first()
        serializer = RegisterUserSerializer(user)
        return Response(serializer.data)

