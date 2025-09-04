from rest_framework import serializers
from users.models import User, PatientProfile, DoctorProfile, DoctorApplication
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from django.db import transaction
from campaigns.models import VaccineCampaign
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
    age = serializers.ReadOnlyField()
    class Meta:
        model = PatientProfile
        fields = ['id','user','age','date_of_birth','blood_group']

class SimpleUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','phone_number']

class DoctorApplicationSerializer(serializers.ModelSerializer):
    certificate = serializers.ImageField(required=False, allow_null=True)
    user = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = DoctorApplication
        fields = ['id','user','qualifications','certificate','license_number','status','applied_at']
        read_only_fields = ['applied_at','status']

class DoctorApprovalSerializer(serializers.ModelSerializer):
    certificate = serializers.ImageField(read_only=True)
    class Meta:
        model = DoctorApplication
        fields = ['id','user','qualifications','certificate','license_number','status','applied_at']
        read_only_fields = ['id','qualifications','license_number','applied_at']
    
    def update(self, instance, validated_data):
        old_status = instance.status
        with transaction.atomic():
            super().update(instance, validated_data)
            new_status = instance.status

            if old_status != new_status and new_status == 'Approved':
                user = instance.user
                if user.role != User.DOCTOR:
                    user.role = User.DOCTOR
                    user.save()
                DoctorProfile.objects.get_or_create(user=user)

        return instance      

class SimpleDoctorSerializers(serializers.ModelSerializer):
    profile_picture = serializers.ImageField()
    bio = SimpleUserSerializers(source='user',read_only=True)
    class Meta:
        model = DoctorProfile
        fields = ['id','bio','specialization','contact','profile_picture']

class DoctorProfileSerializers(serializers.ModelSerializer):
    # profile_picture = serializers.ImageField()
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    # user = UserSerializer(read_only=True)
    class Meta:
        model = DoctorProfile
        # fields = ['id','user','specialization','contact','profile_picture']
        fields = ['id','specialization','contact','profile_picture']

class DoctorParticipatingCampaignsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineCampaign
        fields = ['id','title','start_date','end_date','status']
