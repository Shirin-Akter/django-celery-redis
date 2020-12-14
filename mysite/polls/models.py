from django.db import models
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import tempfile
from django.core.files import File
from gtts import gTTS
# Create your models here.
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
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # def save(self, *args, **kwargs):
    #     imgName, ext = os.path.splitext(self.document.name)
    #     print('ext: ', ext)
    #     if not self.id:
    #         if ext =='.jpg':
    #             self.document = self.compressImage(self.document)
    #         else:
    #             self.document = self.videoupload(self.document)
    #     print('thi sis document print : ',self.document)
    #     tryit = super(Document,self).save(*args, **kwargs)
    #     print('try it :', tryit)
    # def compressImage(self, document):
    #     imageTemproary = Image.open(document)
    #     outputIoStream = BytesIO()
    #     size_100 = (100,100)
    #     # imageTemproary.thumbnail(size_100)
    #     imageTemproaryResized = imageTemproary.resize((100, 100))
    #     imageTemproary.save(outputIoStream, format='JPEG', quality=60)
    #     outputIoStream.seek(0)
    #     document = InMemoryUploadedFile(outputIoStream, 'FileField', "%s.png" % document.name.split('.')[0],
    #                                          'image/png', sys.getsizeof(outputIoStream), None)
    #     print('document here: ', document)
    #     return document
    # def videoupload(self,document):
    #     # document = gTTS(text=self.document, lang='en' , slow=True)
    #     # with tempfile.TemporaryFile(mode='w') as f:
    #     #     document.write_fp(f)
    #     #     file_name = '{}.mp3'.format(self.document)
    #     #     self.document.save(file_name, File(file=f))
    #
    #
    #
    #
    #     vidName, ext1 = os.path.splitext(self.document.name)
    #     outputIoStream = BytesIO()
    #     audiofile = vidName + '.mp3'
    #     document1 = InMemoryUploadedFile(audiofile, 'FileField', "%s.mp3" % document.name.split('.')[0],
    #                                     'audio/mpeg', sys.getsizeof(audiofile), None)
    #     print('thi sis document1 print : ', document1)
    #     return document1


