from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import UploadedContent
from .serializers import UploadedContentSerializer

from .forms import UploadedContentForm
from django.shortcuts import redirect

from django.http import JsonResponse
import datetime

import json 
from django.views.decorators.csrf import csrf_exempt
import os

from django.conf import settings
from django.core.files.storage import default_storage
import uuid

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import UploadedContent

from .models import ChatMessage

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

# Calendar 
def calendar_events(request):
    events = [
        {
            "title": "Team Review",
            "start": str(datetime.date.today()),
        },
        {
            "title": "Deadline - Project Plan",
            "start": str(datetime.date.today() + datetime.timedelta(days=3)),
        },
    ]
    return JsonResponse(events, safe=False)
    

def calendar_test_view(request):
    return render(request, 'content_manager/calendar_test.html')


# Chatbot API
from .langchain_utils import get_langchain_chain  

@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        message = request.POST.get("message", "").strip()
        uploaded_file = request.FILES.get("file")
        ai_reply = ""

        # ⬇️ Handle file upload
        if uploaded_file:
            filename = f"{uuid.uuid4()}_{uploaded_file.name}"
            file_path = os.path.join("uploads", filename)
            save_path = os.path.join(settings.MEDIA_ROOT, file_path)

            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            with default_storage.open(save_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Save to DB
            UploadedContent.objects.create(
                title=uploaded_file.name,
                file=file_path,
                content_type='doc'  # Static for now
            )

            ai_reply += f"✅ Uploaded file: {uploaded_file.name}. "

        # ⬇️ Use LangChain to generate a real response
        if message:
            try:
                chain = get_langchain_chain()
                langchain_response = chain.run(message)
                ai_reply += langchain_response
            except Exception as e:
                ai_reply += f"❌ Error generating response: {str(e)}"
        elif not ai_reply:
            ai_reply = "🤖 You didn't say anything!"

        # ⬇️ Save to DB
        ChatMessage.objects.create(
            user_message=message or "",
            bot_reply=ai_reply
        )

        return JsonResponse({"reply": ai_reply})

    return JsonResponse({"error": "Only POST requests are allowed."}, status=405)




    
#Delete Saved Files
def delete_content(request, content_id):
    content = get_object_or_404(UploadedContent, id=content_id)
    
    if request.method == "POST":
        # Delete file from filesystem
        if content.file and os.path.isfile(content.file.path):
            os.remove(content.file.path)

        # Delete from database
        content.delete()
        messages.success(request, "File deleted successfully.")
    
    return redirect('content_list')

'''
#Save chats
def chatbot_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')
        # Simulate response (replace with real logic)
        bot_reply = f"Echo: {user_message}"

        # Save chat
        ChatMessage.objects.create(user_message=user_message, bot_reply=bot_reply)

        return JsonResponse({'reply': bot_reply})'''

   
#Save Chats Page
def saved_chats(request):
    chats = ChatMessage.objects.order_by('-timestamp')
    return render(request, 'content_manager/saved_chats.html', {'chats': chats})
