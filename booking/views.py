from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from booking.serializers import *
from rest_framework.response import Response
from campaigns.permissions import IsDoctorOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

class CenterViewSet(ModelViewSet):
    queryset = Center.objects.all()
    serializer_class = CenterSerializers
    permission_classes = [IsDoctorOrReadOnly]

class BookingDoseViewSet(ModelViewSet):
    # http_method_names = ['get','patch']
    # queryset = BookingDose.objects.all()
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role == 'Doctor':
            return BookingDose.objects.all()
        return BookingDose.objects.filter(patient=user)

    serializer_class = BookingDoseSerializers

    # def get_permissions(self):
        # if self.request.user.is_staff:
            # return [permissions.IsAdminUser()]
    
    def get_serializer_context(self):
        return {'campaign_id' : self.kwargs.get('pk'), 'user': self.request.user}

class VaccinationRecordViewSet(ModelViewSet):
    queryset = VaccinationRecord.objects.all()
    serializer_class = VaccinationRecordSerializers