from rest_framework import serializers
from .models import *

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields = "__all__"