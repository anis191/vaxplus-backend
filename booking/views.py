from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from booking.serializers import *
from rest_framework.response import Response

class CenterViewSet(ModelViewSet):
    queryset = Center.objects.all()
    serializer_class = CenterSerializers

class BookingDoseViewSet(ModelViewSet):
    queryset = BookingDose.objects.all()
    serializer_class = BookingDoseSerializers
    
    def get_serializer_context(self):
        return {'campaign_id' : self.kwargs.get('pk')}

class VaccinationRecordViewSet(ModelViewSet):
    queryset = VaccinationRecord.objects.all()
    serializer_class = VaccinationRecordSerializers