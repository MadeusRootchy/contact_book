from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
import random


# Create your models here.

class Contact(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='contact')
    full_name = models.CharField(max_length=250,null=True,blank=True)
    relationship = models.CharField(max_length=250,null=True,blank=True)
    email = models.EmailField(max_length=254,null=True,blank=True)
    phone_number = models.CharField(max_length=20,default='')
    address = models.CharField(max_length=1000,default='inconnu',null=True,blank=True)

    def __str__(self):
          return self.full_name



class NewUser(models.Model):
    non = models.CharField(max_length = 255)
    modpas = models.CharField(max_length=255)
    modpas2 = models.CharField(max_length=255)

    
    def __str__(self):
        return self.non

    class Meta:
        verbose_name = 'Itilizate'
        verbose_name_plural = 'Itilizate yo'
