from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from time import time

def make_upload_path(instance, filename):
    """Generates upload path for FileField"""
    res = u"static/uploads/%s-%s" % (str(time()), filename)
    return res

class UploadFile(models.Model):
    FileName = models.CharField(max_length=255)
    File = models.ImageField(upload_to=make_upload_path)
    Uploaded_date = models.DateTimeField(auto_now_add=True)

class TextRecRes(models.Model):
    Rects = models.TextField(max_length=1000)
    Text = models.TextField(max_length=1000)
    FK_UFile = models.ForeignKey(UploadFile) 

class Person(models.Model):
    Name = models.CharField(max_length=100)
    ClassifierName = models.CharField(max_length=255)
    def __unicode__(self):
        return u"%s" % self.Name

class FaceRecRes(models.Model):
    Rects = models.TextField(max_length=1000)
    Class = models.ForeignKey(Person, default=None, null=True, related_name="Class") 
    Mark  = models.ForeignKey(Person, default=None, null=True, related_name="Mark") 
    #Class = models.IntegerField(default=1, validators=[MaxValueValidator(100),MinValueValidator(1)])
    #Mark = models.IntegerField(default=1, validators=[MaxValueValidator(100),MinValueValidator(1)])
    FileName = models.CharField(max_length=255)
    FK_UFile = models.ForeignKey(UploadFile) 

