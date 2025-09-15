from rest_framework import serializers
from campaigns.models import *
from users.models import *
from booking.models import BookingDose, VaccinationRecord
from users.serializers import UserSerializer,DoctorProfileSerializers
from django.urls import reverse
#
class CategorySerializer(serializers.ModelSerializer):
    campaign_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ["id","name","description","campaign_count"]

class VaccineSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = ['id','name','description','total_doses','dose_gap','is_booster','booster_gap','min_age','max_age','manufacturer','approved_date','is_active']

class SimpleVaccineSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = ['id','name','total_doses','dose_gap','is_booster']

class CampaignDoctorsSerializers(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    specialization = serializers.CharField(source='doctor_profile.specialization')
    profile_picture = serializers.ImageField(source='doctor_profile.profile_picture')
    class Meta:
        model = User
        fields = ['id','doctor_profile','profile_picture','name','specialization']
    
    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

class VaccineCampaignSerializers(serializers.ModelSerializer):
    banner = serializers.ImageField(required=False, allow_null=True)
    vaccine_details = SimpleVaccineSerializers(source='vaccine',many=True,read_only=True)
    vaccine = serializers.PrimaryKeyRelatedField(many=True, queryset=Vaccine.objects.filter(is_active=True).only('id', 'name'), write_only=True)
    doctor = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = User.objects.filter(role=User.DOCTOR),
        write_only = True
    )
    class Meta:
        model = VaccineCampaign
        fields = ['id','title','description','category','banner','vaccine','vaccine_details','doctor','is_premium','registration_fee','start_date','end_date','status']
        
class CampaignReviewSerializers(serializers.ModelSerializer):
    # name = serializers.ReadOnlyField(source='patient.first_name')
    name = serializers.SerializerMethodField()
    user_id = serializers.ReadOnlyField(source='patient.id')
    class Meta:
        model = CampaignReview
        fields = ['id','user_id','name','comment','rating']
        read_only_fields = ['campaign']
    
    def get_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"

    def create(self, validated_data):
        campaign_id = self.context['campaign_id']
        user = self.context.get('user')
        
        try:
            campaign = VaccineCampaign.objects.get(pk=campaign_id)
        except VaccineCampaign.DoesNotExist:
            raise serializers.ValidationError("Campaign does not exist.")
        
        if BookingDose.objects.filter(patient=user,campaign=campaign).exists() or VaccinationRecord.objects.filter(patient=user,campaign=campaign).exists():
            review = CampaignReview.objects.create(patient=user,campaign=campaign,**validated_data)
            return review
        else:
            raise serializers.ValidationError("You can't review this camapign. Only booked patient can.")

class SimpleCampaignListSerializer(serializers.ModelSerializer):
    vaccine_details = SimpleVaccineSerializers(source='vaccine',many=True,read_only=True)
    banner = serializers.ImageField()
    class Meta:
        model = VaccineCampaign
        fields = ['id','title','description','banner','vaccine_details','is_premium','start_date','end_date','status']