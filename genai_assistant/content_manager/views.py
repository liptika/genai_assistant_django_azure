from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import UploadedContent
from .serializers import UploadedContentSerializer

from .forms import UploadedContentForm
from django.shortcuts import redirect

#API View

class UploadedContentListCreateView(generics.ListCreateAPIView):
    queryset = UploadedContent.objects.all().order_by('-uploaded_at')
    serializer_class = UploadedContentSerializer

#UI View
    
def home(request):
    return render(request, 'content_manager/home.html')

# Page to upload and manage content
'''def upload_page(request):
    return render(request, 'content_manager/upload.html')'''

#Form Page
def upload_content(request):
    if request.method == 'POST':
        form = UploadedContentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('content_list')
    else:
        form = UploadedContentForm()
    return render(request, 'content_manager/upload.html', {'form': form})

# Page to show all uploaded content
def content_list_page(request):
    uploaded_contents = UploadedContent.objects.all().order_by('-uploaded_at')
    return render(request, 'content_manager/content_list.html', {'uploaded_contents': uploaded_contents})

# Chatbot interface page
def chatbot_page(request):
    return render(request, 'content_manager/chatbot.html')

