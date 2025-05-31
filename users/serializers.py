from rest_framework import serializers
from users.views import User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','address','phone_number','role','nid']
