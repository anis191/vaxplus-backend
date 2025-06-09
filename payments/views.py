from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(GenericViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def list(self, request, *args, **kwargs):
        return Response({
            "message": "Payment integration will be implemented in a future update."
        })
