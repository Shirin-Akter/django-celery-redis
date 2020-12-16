from django import forms
from .models import Document

class UploadFileForm(forms.ModelForm):
    class Meta:
        #title = forms.CharField(max_length=50)
        model = Document
        #file = forms.FileField()
        fields = ('description' , 'document',)
        print('inside forms')

