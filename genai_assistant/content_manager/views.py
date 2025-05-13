from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import UploadedContent
from .serializers import UploadedContentSerializer

class UploadedContentListCreateView(generics.ListCreateAPIView):
    queryset = UploadedContent.objects.all().order_by('-uploaded_at')
    serializer_class = UploadedContentSerializer