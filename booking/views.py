from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from booking.serializers import *
from campaigns.permissions import IsDoctorOrReadOnly
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class CenterViewSet(ModelViewSet):
    queryset = Center.objects.all()
    serializer_class = CenterSerializers
    permission_classes = [IsDoctorOrReadOnly]

class BookingDoseViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'head', 'options']
    serializer_class = BookingDoseSerializers
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter,]
    def filter_queryset(self, queryset):
        if self.request.user.is_staff or self.request.user.role == User.DOCTOR:
            self.search_fields = ['patient__email']
        else:
            self.search_fields = []
        return super().filter_queryset(queryset)

    def get_queryset(self):
        user = self.request.user
        base_query = BookingDose.objects.select_related('patient','campaign','dose_center')
        if user.is_staff or user.role == 'Doctor':
            return base_query
        return base_query.filter(patient=user)
    
    def get_serializer_context(self):
        return {'campaign_id' : self.kwargs.get('pk'), 'user': self.request.user}

class VaccinationRecordViewSet(ModelViewSet):
    http_method_names = ['get','head','options']
    serializer_class = VaccinationRecordSerializers
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        base_query = VaccinationRecord.objects.select_related('patient','campaign','campaign__vaccine')
        if user.is_staff:
            return base_query
        return base_query.filter(patient=self.request.user)

