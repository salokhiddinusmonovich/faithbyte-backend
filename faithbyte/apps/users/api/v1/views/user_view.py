from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from django.http import JsonResponse
from faithbyte.apps.users import models
from ...v1.utils import tools, qury_params
from ..serializers import user_serializers
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
import random
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import uuid
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

user_model = get_user_model()


class UserRegisterView(GenericAPIView):
    serializer_class = user_serializers.UserRegisterSerializer
    permission_classes = [AllowAny]

   
    @swagger_auto_schema(
    operation_description="Update the company profile and user details of the logged-in user.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "first_name": openapi.Schema(type=openapi.TYPE_STRING, description="First name of the user."),
            "last_name": openapi.Schema(type=openapi.TYPE_STRING, description="Last name of the user."),
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email address of the user."),
            "phone": openapi.Schema(type=openapi.TYPE_STRING, description="Phone number of the company."),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="New password for the user."),
        },
        required=["first_name", "last_name", "email", "phone", "password"],
    ),
    )
        
    def post(self, request):
        data = self.request.data
        try:
            user_model.objects.get(email=data.get("email"))
            models.Profile.objects.get(email=data.get("email"))
            return Response({"status": "error", "message": "this email is registered"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        try:
            check_register = models.RegisterCheck.objects.create(**data)
            code = tools.send_verification_code_to_email__second(email=check_register.email)
            check_register.code = code
            check_register.save()
            response_token = tools.encode_email(email=check_register.email)
            return Response({"status": "success", "token": response_token})
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class VerifyUserAccount(GenericAPIView):
    serializer_class = user_serializers.VerifiationCodeSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(manual_parameters=qury_params.get_token())
    
    def post(self, request):
        token = request.GET.get('token')
        email = tools.decode_email(token)
        code = self.request.data.get("verification_code") 
        if not code:
            return Response({"status": "error", "message": "Verification code is missing."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            not_auth_user = models.RegisterCheck.objects.get(email=email)
            if not_auth_user.code == int(code):
                user = user_model.objects.create(username=not_auth_user.first_name,email=not_auth_user.email, password=not_auth_user.password, 
                                                 first_name=not_auth_user.first_name,
                                                 last_name=not_auth_user.last_name,
                                                 is_active=True)
                user.set_password(not_auth_user.password)
                user.save()
                models.Profile.objects.create(user=user,first_name=not_auth_user.first_name,
                                              last_name=not_auth_user.last_name,
                                              email=not_auth_user.email,
                                              phone_number=not_auth_user.phone)
                return Response({"status": "success", "message": "successfully registered"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "message": "invalid verification code"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class CustomTokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Obtain JWT tokens by providing email and password.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            },
            required=['email', 'password'],
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                },
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                },
            ),
            401: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Invalid credentials'),
                },
            ),
        },
    )

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user_model().objects.get(email=email)
            if user.check_password(password):  # checking password
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    'access': access_token,
                    'refresh': str(refresh),
                })
            else:
                return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        except get_user_model().DoesNotExist:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        

