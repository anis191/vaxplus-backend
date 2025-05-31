from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import UserSerializers

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
