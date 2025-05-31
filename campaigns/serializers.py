from rest_framework import serializers
from campaigns.models import *

class CategorySerializer(serializers.ModelSerializer):
    campaign_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ["id","name","description","campaign_count"]

class VaccineSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = ['id','name','total_doses','dose_gap']

class VaccineCampaignSerializers(serializers.ModelSerializer):
    class Meta:
        model = VaccineCampaign
        fields = ['id','doctor','title','description','category','vaccine','start_date','end_date','status']

class CampaignReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = CampaignReview
        fields = ['id','patient','campaign','comment','rating']