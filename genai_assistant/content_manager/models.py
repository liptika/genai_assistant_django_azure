from django.db import models

# Create your models here.
class UploadedContent(models.Model):
    CONTENT_TYPES = (
        ('doc', 'Document'),
        ('link', 'Web Link'),
        ('note', 'Note'),
    )

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


#Model Chat History
class ChatMessage(models.Model):
    user_message = models.TextField()
    bot_reply = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - User: {self.user_message}"
    

#Search History
class SearchHistory(models.Model):
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query


