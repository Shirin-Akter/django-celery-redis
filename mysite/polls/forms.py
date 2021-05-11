from django import forms
from .models import Document, Blog, Comment

class UploadFileForm(forms.ModelForm):
    class Meta:
        #title = forms.CharField(max_length=50)
        model = Document
        #file = forms.FileField()
        fields = ('description' , 'document',)
        # print('inside forms')


class BlogForm(forms.ModelForm):
    class Meta():
        model = Blog
        fields = ('author','title', 'context')

        # widgets = {
        #     'title':forms.TextInput(attrs)
        # }

class CommentForm():
    class Meta():
        model = Comment
        fields = ('author','text')





