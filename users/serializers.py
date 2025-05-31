from rest_framework import serializers
from users.views import User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
