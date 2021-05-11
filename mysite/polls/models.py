from datetime import datetime

from django.db import models
from django.contrib.auth.models import  User
# Create your models here.
from django.urls import reverse
from ckeditor.fields import RichTextField


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >=timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    # document = models.FileField(upload_to=None)
    document = models.FileField(upload_to=None, max_length=None)
    digital_ocean_url = models.CharField(max_length=250, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.digital_ocean_url
    def __str__(self):
        return self.description

class Blog(models.Model):
    options = (
        ('Draft', 'draft'),
        ('Published', 'published'),
    )
    #what fields do i need
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=100, blank=True)
    excerpt = models.CharField(max_length=100, blank=True)
    # img = models.FileField(upload_to=None, max_length=None)
    slug = models.SlugField(max_length=100, blank=True)
    context = models.TextField(max_length=100, blank=True, null= True)
    # context1 = RichTextField(blank = True, null = True)
    status = models.CharField(max_length=100, blank=True, choices= options, default= 'Draft')
    published = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        ordering = ('-published',)
    def publish(self):
        self.published >=timezone.now() - datetime.timedelta(days=1)
        self.save()
    def get_absolute_url(self):
        return reverse('post_single', args=[self.slug])
    def approve_comments(self):
        return self.comments.filter(approved_comments=True)

    def __str__(self):
        return self.title
class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comment')
    author = models.CharField(max_length = 100)
    text = models.TextField()
    create_date = models.DateTimeField( auto_now_add = True )
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment =True
        self.save()
    def get_absolute_url(self):
        return reverse('home')
    def __str__(self):
        return self.text








