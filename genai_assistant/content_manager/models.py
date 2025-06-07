from django.db import models

# Create your models here.
class UploadedContent(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=50)
    extracted_text = models.TextField(blank=True, null=True)
    search_id = models.CharField(max_length=100, blank=True, null=True)  # Added for Azure AI Search reference
    vector_id = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.title
    


#Model Chat History
class ChatMessage(models.Model):
    user_message = models.TextField()
    bot_reply = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - User: {self.user_message}"
    




