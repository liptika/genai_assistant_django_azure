from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_content, name='upload'),
    path('content_list/', views.content_list_page, name='content_list'),
    path('chatbot/', views.chatbot_page, name='chatbot'),
]
