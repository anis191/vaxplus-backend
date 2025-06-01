from django.urls import path,include
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from users.views import *
from campaigns.views import *
from booking.views import *

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('patients', PatientProfileViewSet, basename='patient')
router.register('doctors', DoctorProfileViewSet, basename='doctor')
router.register('categories', CategoryViewSet)
router.register('campaigns', VaccineCampaignViewSet, basename='campaign')
router.register('vaccines', VaccineViewSet, basename='vaccine')
router.register('centers', CenterViewSet, basename='center')
router.register('booking_doses', BookingDoseViewSet, basename='booking_dose')
router.register('vaccination_records', VaccinationRecordViewSet, basename='vaccination_record')


campaign_router = routers.NestedDefaultRouter(router, 'campaigns', lookup='campaign')
# campaign_router.register('vaccines', VaccineViewSet, basename='campaign-vaccines')
campaign_router.register('reviews', CampaignReviewViewSet, basename='campaign-review')

urlpatterns = [
    path('',include(router.urls)),
    path('',include(campaign_router.urls)),
]