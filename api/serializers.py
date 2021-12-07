from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stations
        fields = '__all__'