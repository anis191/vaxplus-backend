from django.contrib import admin
from campaigns.models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Vaccine)
admin.site.register(VaccineCampaign)
admin.site.register(CampaignReview)