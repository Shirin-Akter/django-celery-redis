from django.contrib import admin
from .models import Question
from .models import Document

admin.site.register(Question)
admin.site.register(Document)
# Register your models here.
