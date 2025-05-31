from rest_framework import serializers
from campaigns.models import *
from users.models import *
from users.serializers import UserSerializers,DoctorProfileSerializers

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
    doctor_detail = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = VaccineCampaign
        fields = ['id','title','description','category','vaccine','vaccine_details','doctor','doctor_detail','start_date','end_date','status']
        extra_kwargs = {
            'doctor' : {'write_only':True}
        }
    
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
        fields = ['id','patient','campaign','comment','rating']
        read_only_field = ['campaign']
    
    def create(self, validated_data):
        campaign_id = self.context['campaign_id']
        review = CampaignReview.objects.create(campaign_id=campaign_id, **validated_data)
        return review