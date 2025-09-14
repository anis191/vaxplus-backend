from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings
from rest_framework import status
import uuid
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PaymentsFilter
# from users.paginations import PaymentsPagination

class PaymentViewSet(ModelViewSet):
    http_method_names = ['get','head','options']
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentsFilter
    # pagination_class = PaymentsPagination

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view',False):
            return Payment.objects.none()

        base_query = Payment.objects.select_related('patient','campaign')
        if self.request.user.is_staff:
            return base_query
        return base_query.filter(patient = self.request.user)
    
    @swagger_auto_schema(
        operation_summary="List payments history",
        operation_description="""
        - **Admin** users can view **all** payments.  

        - **Patients** can view **only their own** payments.  

        - Each payment is linked to a **Campaign** and the **Patient**.  
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a payment details by ID",
        operation_description="""
        - **Admin** users can retrieve any payment by its ID.  

        - **Patients** can retrieve **only their own** payments.  

        - Useful to check the details of a specific payment.  
        """
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    user = request.user
    campaign = request.data.get('campaign')
    amount = request.data.get('amount')

    if Payment.objects.filter(patient=user, campaign_id=campaign, status=Payment.SUCCESS).exists():
        return Response({"error": "You have already paid for this campaign."},
                        status=status.HTTP_400_BAD_REQUEST)

    tran_id = f"txn_{user.id}{str(uuid.uuid4())[:12]}"

    payment = Payment.objects.create(
        patient = user,
        campaign_id = campaign,
        amount = amount,
        status = Payment.PENDING,
        transaction_id = tran_id
    )

    sslcz = SSLCOMMERZ(settings.SSL_COMMERZ_SETTINGS)

    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = tran_id
    post_body['success_url'] = "http://127.0.0.1:8000/api/v1/payment/success/"
    post_body['fail_url'] = "http://127.0.0.1:8000/api/v1/payment/fail/"
    post_body['cancel_url'] = "http://127.0.0.1:8000/api/v1/payment/cancel/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f"{user.first_name} {user.last_name}"
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = user.phone_number
    post_body['cus_add1'] = user.address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Vaccine"
    post_body['product_category'] = "Medicine"
    post_body['product_profile'] = "general"

    response = sslcz.createSession(post_body) # API response
    # print(response)

    if response.get("status") == "SUCCESS":
        return Response({"payment_url" : response['GatewayPageURL']})
    return Response({"error" : "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def payment_success(request):
    tran_id = request.data.get("tran_id")
    try:
        payment = Payment.objects.get(transaction_id = tran_id)
        payment.status = Payment.SUCCESS
        payment.save()
        return Response({"message": "Payment Successful", "tran_id": tran_id})
    except Payment.DoesNotExist:
        return Response({"error": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def payment_cencel(request):
    tran_id = request.data.get("tran_id")
    try:
        payment = Payment.objects.get(transaction_id = tran_id)
        payment.delete()
        return Response({"message" : "Payment Cancelled"})
    except Payment.DoesNotExist:
        return Response({"error": "Payment record not found"}, status=404)
    # return redirect(f"{main_settings.FRONTEND_URL}/dashboard/orders/")

@api_view(['POST'])
def payment_fail(request):
    tran_id = request.data.get("tran_id")
    try:
        payment = Payment.objects.get(transaction_id = tran_id)
        payment.status = Payment.FAILED
        payment.save()
        return Response({"message": "Payment Failed", "tran_id": tran_id})
    except Payment.DoesNotExist:
        return Response({"error": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)
    # return redirect(f"{main_settings.FRONTEND_URL}/dashboard/orders/")

class HasPaidCampaign(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, campaign_id):
        user = request.user
        has_paid = Payment.objects.filter(patient=user, campaign_id=campaign_id, status=Payment.SUCCESS).exists()
        return Response({"hasPaid" : has_paid})