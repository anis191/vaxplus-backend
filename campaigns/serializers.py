from rest_framework import serializers
from campaigns.models import *
from users.models import *
from booking.models import BookingDose, VaccinationRecord
from users.serializers import UserSerializer,DoctorProfileSerializers

class CategorySerializer(serializers.ModelSerializer):
    campaign_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ["id","name","description","campaign_count"]

class VaccineSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = ['id','name','description','total_doses','dose_gap']

class VaccineCampaignSerializers(serializers.ModelSerializer):
    vaccine_details = VaccineSerializers(source='vaccine',read_only=True)
    vaccine = serializers.PrimaryKeyRelatedField(queryset=Vaccine.objects.all(),write_only=True)
    doctor = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.filter(role=User.DOCTOR),
        write_only = True
    )
    doctor_detail = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = VaccineCampaign
        fields = ['id','title','description','category','vaccine','vaccine_details','doctor','doctor_detail','start_date','end_date','status']
    
    def get_doctor_detail(self, obj):
        specialization = None
        if hasattr(obj.doctor, 'doctor_profile'):
            specialization = obj.doctor.doctor_profile.specialization
        return{
            'name' : obj.doctor.get_full_name(),
            'specialization' : specialization
        }

class CampaignReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = CampaignReview
        fields = ['id','comment','rating']
        read_only_fields = ['campaign']
    
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