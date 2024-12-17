
from rest_framework import serializers

from ....models import *


class VerifiationCodeSerializer(serializers.Serializer):
    verification_code = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        fields = "__all__"


class UserRegisterSerializer(serializers.Serializer):
    
    class Meta:
        models = RegisterCheck
        fields = ("first_name", "last_name", "email", "phone", "password")