from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from booking.serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response

class CenterViewSet(ModelViewSet):
    queryset = Center.objects.all()
    serializer_class = CenterSerializers

class BookingDoseViewSet(ModelViewSet):
    queryset = BookingDose.objects.all()
    # serializer_class = BookingDoseSerializers

    @action(detail=True, methods=['post'])
    def booked(self, request, pk=None):
        campaign = self.get_object()
        serializer = SimpleBookingDoseSerializers(
            data=request.data,
            context = {'campaign_id' : campaign.pk}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status' : 'Booked the campaign'})
    
    def get_serializer_class(self):
        if self.action == 'booked':
            return SimpleBookingDoseSerializers
        return BookingDoseSerializers
    
    def get_serializer_context(self):
        return {'campaign_id' : self.kwargs.get('pk')}
