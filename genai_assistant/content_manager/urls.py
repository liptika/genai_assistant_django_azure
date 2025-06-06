from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_content, name='upload'),
    path('content_list/', views.content_list_page, name='content_list'),
    path('chatbot/', views.chatbot_page, name='chatbot'),
    path('calendar/events/', views.calendar_events, name='calendar_events'),
    path('calendar-test/', views.calendar_test_view, name='calendar_test'),
    path('chatbot_api/', views.chatbot_api, name='chatbot_api'),
    path('content/delete/<int:content_id>/', views.delete_content, name='delete_content'),
    path('saved_chats/', views.saved_chats, name='saved_chats'),
    path('explore/', views.explore_page, name='explore_page'),
    path('explore/query/', views.explore_api, name='explore_api'),
]
