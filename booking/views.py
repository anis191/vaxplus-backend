from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from booking.serializers import *
from campaigns.permissions import IsDoctorOrReadOnly
from rest_framework import permissions

class CenterViewSet(ModelViewSet):
    queryset = Center.objects.all()
    serializer_class = CenterSerializers
    permission_classes = [IsDoctorOrReadOnly]

class BookingDoseViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'head', 'options']
    serializer_class = BookingDoseSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role == 'Doctor':
            return BookingDose.objects.all()
        return BookingDose.objects.filter(patient=user)
    
    def get_serializer_context(self):
        return {'campaign_id' : self.kwargs.get('pk'), 'user': self.request.user}

class VaccinationRecordViewSet(ModelViewSet):
    http_method_names = ['get','head','options']
    serializer_class = VaccinationRecordSerializers
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return VaccinationRecord.objects.all()
        return VaccinationRecord.objects.filter(patient=self.request.user)

