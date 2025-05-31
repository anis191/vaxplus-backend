from rest_framework import serializers
from users.models import User, PatientProfile, DoctorProfile

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','address','phone_number','role','nid']

class PatientProfileSerializers(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    class Meta:
        model = PatientProfile
        fields = ['id','user','date_of_birth','blood_group']

class DoctorProfileSerializers(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    class Meta:
        model = DoctorProfile
        fields = ['id','user','specialization','contact','profile_picture']
