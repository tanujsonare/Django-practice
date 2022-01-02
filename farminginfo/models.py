from django.db import models
from django.utils import timezone


# Create your models here.
class account_info(models.Model):
    fullname = models.CharField(max_length =30)
    email = models.CharField(max_length =50)
    password = models.CharField(max_length = 30)
    date_of_creation = models.DateTimeField(null=True,blank=True)
    date_of_modification = models.DateTimeField(null = True,blank=True)

class crops_info(models.Model):
    cropsname = models.CharField(max_length= 30)
    crops_description = models.CharField(max_length=100)
    photo = models.ImageField(upload_to = 'media/images/',blank = True ,null = True)

class crop_detail(models.Model):
    State_Name = models.CharField(max_length=30,null=True,blank=True)
    District_Name = models.CharField(max_length=30,null=True,blank=True)
    Crop_Year = models.IntegerField(null=True,blank=True)
    Season = models.CharField(max_length=20 ,null=True,blank=True)
    Crop = models.CharField(max_length=20,null=True,blank=True)
    Area = models.IntegerField(null=True,blank=True)
    Production = models.IntegerField(null=True,blank=True)
    date_of_creation = models.DateTimeField(default=timezone.now ,null=True,blank=True)
    date_of_modification = models.DateTimeField(default=timezone.now ,null = True,blank=True)

    



