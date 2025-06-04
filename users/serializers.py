from rest_framework import serializers
from users.models import User, PatientProfile, DoctorProfile
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
#
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','email','password','first_name','last_name','address','phone_number','nid']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = ['id','first_name','last_name','email','address','phone_number']

class PatientProfileSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = PatientProfile
        fields = ['id','user','age','date_of_birth','blood_group']

class SimpleUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number']

class SimpleDoctorSerializers(serializers.ModelSerializer):
    bio = SimpleUserSerializers(source='user',read_only=True)
    class Meta:
        model = DoctorProfile
        fields = ['id','bio','specialization','contact','profile_picture']

class DoctorProfileSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = DoctorProfile
        fields = ['id','user','specialization','contact','profile_picture']
