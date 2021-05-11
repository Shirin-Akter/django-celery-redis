from django.contrib import admin
from .models import Question
from .models import Document
from .models import Blog
from django import forms
from ckeditor.widgets import CKEditorWidget

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','slug', 'status')
# class BlogAdminForm(forms.ModelForm):
#     body = forms.CharField(widget=CKEditorWidget())
#     class Meta:
#         model = Blog
admin.site.register(Question)
admin.site.register(Document)
admin.site.register(Blog, BlogAdmin)
# Register your models here.
