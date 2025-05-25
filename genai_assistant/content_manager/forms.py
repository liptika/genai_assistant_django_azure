from django import forms
from .models import UploadedContent

class UploadedContentForm(forms.ModelForm):
    class Meta:
        model = UploadedContent
        fields = ['title', 'file']
