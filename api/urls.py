from django.urls import path,include
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from users.views import UserViewSet
from campaigns.views import *

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('campaigns', VaccineCampaignViewSet, basename='campaign')
router.register('vaccines', VaccineViewSet)

campaign_router = routers.NestedDefaultRouter(router, 'campaigns', lookup='campaign')
campaign_router.register('reviews', CampaignReviewViewSet, basename='campaign-review')

urlpatterns = [
    path('',include(router.urls)),
    path('',include(campaign_router.urls)),
]