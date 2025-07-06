from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Owner, Pharmacy
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from datetime import datetime, timezone
from djoser.serializers import UserCreateSerializer
import logging

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','email', 'password']
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False, 'min_length': 8, 'write_only':True}
            }

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id','username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'required': True, 'allow_blank': False, 'min_length': 8, 'write_only':True}
            }   


class OwnerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Owner
        fields = ['user', 'gender','phone', 'nationalID']
        extra_kwargs = {
            'gender': {'required': True, 'allow_blank': False},
            'phone': {'required': True, 'allow_blank': False},
            'nationalID': {'required': True, 'allow_blank': False},
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        owner = Owner.objects.create(user=user, **validated_data)

        return owner
    

class PharmacySerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, style={"input_type":"password"})
    class Meta:
        model = Pharmacy
        fields = ['id', 'name', 'city', 'latitude', 'longitude', 'license_number','number_sells','number_buys', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True, 'style':{"input_type":"password"}}
        }
    
    def validate(self,data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        pharmacy = Pharmacy(**validated_data)
        pharmacy.set_password(validated_data['password'])
        pharmacy.save()
        return pharmacy
     

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)
        self.fields['email'] = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    refresh=self.get_token(user)
                    return {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                else:
                    raise serializers.ValidationError('Incorrect Password')
            except User.DoesNotExist:

                raise serializers.ValidationError('No user found with this email.')
            
            raise serializers.ValidationError('Must provide email and password')   
        

class PharmacyLoginSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def validate(self, data):
        name = data.get('name')
        password = data.get('password')

        try:
            pharmacy = Pharmacy.objects.get(name=name)
        except Pharmacy.DoesNotExist:
            raise serializers.ValidationError({"name": "Not Fount Pharmacy With This Name!"})
        
        if not pharmacy.check_password(password):
            raise serializers.ValidationError({"password": "Incorrect Password"})
        data['pharmacy'] = pharmacy
        return data