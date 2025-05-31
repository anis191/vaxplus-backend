from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import *

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

class PatientProfileViewSet(ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializers

class DoctorProfileViewSet(ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializers