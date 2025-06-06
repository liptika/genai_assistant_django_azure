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

from .utils import extract_dates_and_references_from_file

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dateutil import parser

from docx import Document
from pptx import Presentation

from .models import SearchHistory
from django.db.models import Count
import requests

#API View

class UploadedContentListCreateView(generics.ListCreateAPIView):
    queryset = UploadedContent.objects.all().order_by('-uploaded_at')
    serializer_class = UploadedContentSerializer

#UI View
    
def home(request):
    return render(request, 'content_manager/home.html', {
        'weather_api_key': settings.WEATHER_API_KEY
    })


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
'''def calendar_events(request):
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
    return JsonResponse(events, safe=False)'''

def extract_dates_from_text(text):
    from dateutil.parser import parse
    events = []
    lines = text.split('\n')

    for line in lines:
        try:
            date = parse(line, fuzzy=True)

            # Determine category based on keywords
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in ["meeting", "review", "project", "deadline", "strategy"]):
                category = "professional"
                color = "#87CEFA"  # Light Blue
            elif any(keyword in line_lower for keyword in ["birthday", "anniversary", "party", "doctor", "appointment", "family", "friend"]):
                category = "personal"
                color = "#FFB6C1"  # Light Pink
            else:
                category = "general"
                color = "#D3D3D3"  # Light Gray for uncategorized

            events.append({
                "title": line.strip()[:50],
                "start": date.date().isoformat(),
                "category": category,
                "color": color
            })

        except:
            continue

    return events


def analyze_document(file_path):
    endpoint = settings.AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
    key = settings.AZURE_DOCUMENT_INTELLIGENCE_KEY
    client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-read", document=f)
        result = poller.result()

    content = ""
    for page in result.pages:
        for line in page.lines:
            content += line.content + "\n"
    return content

def calendar_events(request):
    events = []
    uploaded = UploadedContent.objects.all()

    for item in uploaded:
        if item.file:
            file_path = item.file.path
            ext = os.path.splitext(file_path)[1].lower()

            try:
                if ext == ".txt":
                    # Direct read for .txt
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()
                elif ext in [".pdf", ".jpg", ".jpeg", ".png", ".tiff", ".xlsx"]:
                    text = analyze_document(file_path)
                elif ext == ".docx":
                    doc = Document(file_path)
                    text = "\n".join([para.text for para in doc.paragraphs])
                elif ext == ".pptx":
                    prs = Presentation(file_path)
                    text_runs = []
                    for slide in prs.slides:
                        for shape in slide.shapes:
                            if hasattr(shape, "text"):
                                text_runs.append(shape.text)
                    text = "\n".join(text_runs)
                else:
                    print(f"⚠️ Skipped unsupported file type: {file_path}")
                    continue

                extracted = extract_dates_from_text(text)
                events.extend(extracted)

            except Exception as e:
                print(f"❌ Error processing {item.title}: {e}")
                continue

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






@csrf_exempt
def explore_api(request):
    if request.method == "POST":
        query = request.POST.get("query", "").strip()

        if not query:
            return JsonResponse({"error": "No input provided."}, status=400)

        try:
            
            chain = get_langchain_chain()
            response = chain.run(query)

            return JsonResponse({"response": response})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed."}, status=405)

def explore_page(request):
    return render(request, 'content_manager/explore.html')