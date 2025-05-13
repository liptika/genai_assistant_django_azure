from rest_framework import serializers
from .models import UploadedContent

class UploadedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedContent
        fields = '__all__'